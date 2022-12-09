import configparser
import datetime
import json
import logging
import os
import pickle
import socket
import sys
import threading
import time
import uuid
import subprocess
import psycopg2
import psycopg2.extras
from consts import ClientRanks, ClientStatus, JobStatus
from server_utils import CapoomCommand, CapoomResponse, CapoomWork
from logger import setup_logger
import google_chat
from get_credentials import get_credentials


logger = setup_logger("server.log")

SAVE_PATH = "P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{version}/Objects/"
VERSION_PATH = "P:/pipeline/standalone/version.ini"


GET_JOB = """SELECT * FROM "Jobs" WHERE job_uuid = %s"""
UPDATE_JOB_STATUS = """UPDATE "Jobs" SET status = %s WHERE id = %s"""
UPDATE_JOB_END_TIME = """UPDATE "Jobs" SET end_time = %s WHERE id = %s"""
UPDATE_JOB_COUNT = """UPDATE "Jobs" SET count = %s WHERE id = %s"""
UPDATE_JOB_REMAINING = """UPDATE "Jobs" SET remaining = %s WHERE id = %s"""
UPDATE_JOB_PRIORITY = """UPDATE "Jobs" SET priority = %s WHERE id = %s"""
UPDATE_JOB_WORKERS = """UPDATE "Jobs" SET workers = %s WHERE id = %s"""


# UPDATE_JOB = """UPDATE "Jobs" SET status=%s, count=%s, remaining=%s WHERE id = %s"""
CREATE_JOB = """INSERT INTO "Jobs" (project_id, type, remaining, count, status, priority, version, assigner, data, job_uuid, start_time, workers) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"""

    

class CapoomServer():
    def __init__(self):
        
        # Server socket
        self.sock = None
        
        self.addr = socket.gethostname()
        self.port = 18812
        self.max_data = 16384000
        self.timeout = .05
        
        # This stores all commands sent from the admin
        self.commands = []
        self.temp_commands = []
        
        # This stores the actual sockets
        self.all_connections = []
        
        self.all_socks_uuid = {}

        # Added later on
        self.all_stats = {}
        self.all_ranks = {}
        self.assigned = []

        # Database connection
        self.db_conn = None
        self.db_cur = None

        # Command settings


        # TODO implement this
        self.commandTimeout = 10 # In minutes
        self.commandTimeout = self.commandTimeout * 60 # Converted to seconds


        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            logger.critical("Socket creation error: " + str(msg))

        # Bind socket to port
        try:
            self.sock.bind((self.addr, self.port))
            self.sock.listen()
            
            self.sock.setblocking(True) # Prevent timeout
        except socket.error as msg:
            logger.critical("Socket Binding error" + str(msg) + "\n" + "Retrying...")

        # Get database credentials
        try:
            credentials = get_credentials()
            dbname = credentials["db_name"]
            dbuser = credentials["db_user"]
            dbpassword = credentials["db_password"]
            dbhost = credentials["db_host"]
            dbport = credentials["db_port"]
        except Exception as e:
            logger.critical(f"Error getting credentials: {e}")

        # Connect to database
        try:
            

            self.db_conn = psycopg2.connect(f"dbname={dbname} user={dbuser} password={dbpassword} host={dbhost} port={dbport}")

            self.db_cur = self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            psycopg2.extras.register_uuid()
        except Exception as e:
            logger.critical(f"Database connection error: {e}")
    
    def get_active_jobs(self):
        return
        self.db_cur.execute("""SELECT * FROM "Jobs" WHERE status = 'active' ORDER BY priority DESC""")
        self.commands = self.db_cur.fetchall()

    # Handling connection from multiple clients and saving to a list
    def accepting_connections(self):
        # Close already existing connections
        for c in self.all_connections:
            c.close()
        del self.all_connections[:]
        self.all_socks_uuid.clear()

        # Accept new connections
        while True:
            try:
                conn, address = self.sock.accept()
                
                # Save the connection
                self.all_connections.append(conn)
                random_uuid = str(uuid.uuid4())
                self.all_socks_uuid[random_uuid] = conn
                logger.info("Connection has been established :" + address[0])

                self.add_new_sock_to_cmds(conn)
                
                # Adding ip to ini file
                self.chk_add_ip_to_ini(address[0])


            except socket.error as e:
                logger.error(f"Error accepting connections with: {e}")
                pass

    def chk_add_ip_to_ini(self, IPAddr):
        # Add ip to IndividualUpdates if not already there
        try:
            config = configparser.ConfigParser()
            version_file = config.read(VERSION_PATH)
            if version_file:
                if IPAddr not in config["IndividualUpdates"].keys():
                    config["IndividualUpdates"][IPAddr] = "false"
                    with open(VERSION_PATH, 'w') as configfile:
                        config.write(configfile)
        except Exception as e:
            logger.critical(f"Error adding IP to ini: {e}")

        


    def get_sock_uuid(self, sock):
        for key, value in self.all_socks_uuid.items():
            if value == sock:
                return key

    def get_sock_from_uuid(self, uuid):
        for key, value in self.all_socks_uuid.items():
            if key == uuid:
                return value

    def get_assigned_CapoomWork_by_sockUUID(self, sockUUID):
        for assigned in self.assigned:
            if assigned.sock_uuid == sockUUID:
                return assigned

    def get_assigned_CapoomWork_by_cmduuid_workid(self, cmduuid, workid):
        for assigned in self.assigned:
            if assigned.cmd_uuid == cmduuid and assigned.work_id == workid:
                return assigned
                
    #Remove disconnected sockets 
    def remove_sock(self,s,message):

            disconnected_address = s.getpeername()
            disconnected_rank = self.all_ranks[self.get_sock_uuid(s)]
            self.all_connections.remove(s)

            s_uuid = self.get_sock_uuid(s)

            if s_uuid in self.all_socks_uuid:
                logger.debug(f"Removing {disconnected_address} from all_socks_uuid")
                self.all_socks_uuid.pop(s_uuid)
            if s_uuid in self.all_stats:
                logger.debug(f"Removing {disconnected_address} from all_stats")
                self.all_stats.pop(s_uuid)
            if s_uuid in self.all_ranks:
                logger.debug(f"Removing {disconnected_address} from all_ranks")
                self.all_ranks.pop(s_uuid)
            if self.get_assigned_CapoomWork_by_sockUUID(s_uuid):
                logger.debug(f"Removing {disconnected_address} work from assigned")
                self.assigned.remove(self.get_assigned_CapoomWork_by_sockUUID(s_uuid))

            self.send_cl_to_admins()


            s.close()
            logger.warning(f'disconnected ip:{disconnected_address[0]} rank: {disconnected_rank} reason: {message}')

    #Save and get assigned jobs and their machine ips as pickle
    def saveAssignedCommands(data):
        with open('assigned', 'wb') as handle:
            pickle.dump(data, handle)
    
    def loadAssignedCommands():
        with open('assigned', 'rb') as handle:
            loaded = pickle.load(handle)
            return loaded
            
    #Get socket from ip
    def get_sock_from_ip(self, ip):
        
        for sock in self.all_connections:
            sock_uuid = self.get_sock_uuid(sock)

            if self.all_ranks[sock_uuid] == ClientRanks.CLIENT.value:
                if sock.getpeername()[0] == ip:
                    return sock

    def send_cl_to_admins(self):
        for conn in self.all_connections:
            try:
                sock_uuid = self.get_sock_uuid(conn)
                if sock_uuid in self.all_ranks:
                    if self.all_ranks[sock_uuid] == ClientRanks.ADMIN.value:

                        all_client_ips = {self.get_sock_from_uuid(x).getpeername()[0]:self.all_stats[x] for x in self.all_stats}
                        conn.send(pickle.dumps(("clients", all_client_ips)))
            except socket.error as e:
                logger.error(f"Error sending clients to admins: {e}")
                pass

    def clear_cmds(self):
        
        for command in self.commands.copy():
            
            self.rem_cmds(command, JobStatus.CANCELLED.value)
            logger.info(f"Command with {command.data['projectid']} project id removed from queue")
            self.send_cmds_to_db()
            
        #clear assigneds
        self.assigned = []

    def rem_cmds(self, command, reason):

        try:
            try:
                self.db_cur.execute(GET_JOB, (command.uuid,))
                job = self.db_cur.fetchone()
                if job:
                    self.db_cur.execute(UPDATE_JOB_STATUS, (reason, job["id"]))
                    self.db_conn.commit()
                    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.db_cur.execute(UPDATE_JOB_END_TIME, (end_time, job["id"]))
                    self.db_conn.commit()

            except Exception as e:
                logger.error(f"Error updating job status: {e}")

            self.commands.remove(command)

            logger.info(f"Command removed with project id: {command.data['projectid']}")
            self.send_cmds_to_db()
        except Exception as e:
            logger.error(f"Command remove error: {e}")


    def send_cmds_to_db(self):
        # return
        if self.commands:
            # try:
                
                for command in self.commands.copy():
                    assigner = command.assigner
                    status = command.status
                    workers = command.data["ips"]

                    self.db_cur.execute(GET_JOB, (command.uuid,))
                    job_to_update = self.db_cur.fetchone()
                    if job_to_update:
                        # logger.info("UPDATE PARAMS", "status", command.status, "count", command.count, "remaining", len(command.remaining), "id", job_to_update["id"])
                        # logger.debug("Assigner is: " + str(assigner) + "Status is: " + str(status))
                        
                        if job_to_update["count"] != command.count:
                            self.db_cur.execute(UPDATE_JOB_COUNT, (command.count, job_to_update["id"]))
                            self.db_conn.commit()
                            logger.info("Updated job count > " + str(command.count))

                        if job_to_update["status"] != command.status:
                            self.db_cur.execute(UPDATE_JOB_STATUS, (command.status, job_to_update["id"]))
                            self.db_conn.commit()
                            logger.info("Updated job status > " + str(command.status))
                            
                        if job_to_update["remaining"] != len(command.remaining):
                            self.db_cur.execute(UPDATE_JOB_REMAINING, (len(command.remaining), job_to_update["id"]))
                            self.db_conn.commit()
                            logger.info("Updated job remaining")
                        if job_to_update["workers"] != workers:
                            self.db_cur.execute(UPDATE_JOB_WORKERS, (workers, job_to_update["id"]))
                            self.db_conn.commit()
                            logger.info("Updated job workers")
                        if job_to_update["priority"] != command.priority:
                            self.db_cur.execute(UPDATE_JOB_PRIORITY, (command.priority, job_to_update["id"]))
                            self.db_conn.commit()
                            logger.info("Updated job priority > " + str(command.priority))
                    else:

                        # Creating new job
                        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        clean_data = command.data.copy()
                        clean_data.pop("workids_tries")
                        clean_data.pop("ips")
                        clean_data.pop("error_count")
                        try:
                            clean_data.pop("target_uuid")
                        except Exception:
                            pass

                        self.db_cur.execute(CREATE_JOB, (int(command.data["projectid"]),
                                                        command.type,
                                                        len(command.remaining),
                                                        command.count, 
                                                        status,
                                                        command.priority,
                                                        command.version, 
                                                        assigner, 
                                                        json.dumps(clean_data),
                                                        command.uuid,
                                                        start_time,
                                                        workers
                                                        )
                                            )
                        self.db_conn.commit()
            
       

    def read_cmds(self, unpickled):

        unpickled.init_remaining()

        skip = unpickled.data["skip"]
        structure = unpickled.data["structure"]
        projectid = unpickled.data["projectid"]
        version = str(unpickled.version).zfill(4)
        
       

        # Skip exists
        if skip == True:
            logger.info("Skip enabled")
           
            done = []
            #Get lines from finished.txt
            if os.path.isfile(SAVE_PATH.format(structure=structure, project_id=projectid, version=version) + "finished.txt"):
                
                with open(SAVE_PATH.format(structure=structure, project_id=projectid, version=version) + "finished.txt", "r") as f:
                    lines = f.readlines()
                    # remove whitespace characters like `\n` at the end of each line
                    lines = [x.strip() for x in lines]
                    
                    for workid in unpickled.remaining:
                        
                        # done = self.check_done(projectid, workid)
                        workidstr = str(workid)
                        if workidstr in lines:
                            done.append(workid)
                            logger.info(f"Work {workid} already done, removed from remaining")
                    unpickled.remaining = [x for x in unpickled.remaining if x not in done]

        # self.temp_commands.append(unpickled)

        unpickled.data["ips"] = unpickled.sockets
        unpickled.sockets = [self.get_sock_from_ip(x) for x in unpickled.data["ips"]]
        
        # Default all the workid keys to workid and values to 0
        unpickled.data["workids_tries"] = {x:0 for x in unpickled.remaining}

        unpickled.data["error_count"] = 0
        
        self.commands.append(unpickled)

        logger.info(f"Command added: {unpickled.type} {unpickled.data['projectid']} {unpickled.version} {unpickled.count}")
        # google_chat.send_message(f"Command added: {unpickled.type} {unpickled.data['projectid']} {unpickled.version} {unpickled.count}")
        
        self.sort_commands()
        self.send_cmds_to_db()
    
    
    def sort_commands(self):
        self.commands.sort(key=lambda x: x.priority, reverse=True)
        self.send_cmds_to_db()
        logger.debug("Commands sorted")
        
        

    def add_new_sock_to_cmds(self, conn):
        for cmd in self.commands:
            if conn not in cmd.sockets and conn.getpeername()[0] in cmd.data["ips"]:
                cmd.sockets.append(conn)
                logger.info(f"Added new sock to command {cmd.type} {cmd.data['projectid']} {cmd.version} {cmd.count}")

    def rm_assigned_CapoomWork_by_cmd_id_and_work_id(self, cmd_uuid, work_id):
        for work in self.assigned:
            if work.cmd_uuid == cmd_uuid and work.work_id == work_id:
                self.assigned.remove(work)
                logger.info(f"Removed assigned work {work_id}")
                break

    def read_responses(self, unpickled, sock):
        sock_uuid = self.get_sock_uuid(sock)
        ip = sock.getpeername()[0]

        

        # This handles the status of the machine, if it is available or not
        if unpickled.type == "status":
            status = unpickled.data["status"]
            self.all_stats[sock_uuid] = status
            self.send_cl_to_admins()
        
        # This handles the rank of the machine, if it is admin or a slave
        elif unpickled.type == "rank":
            rank = unpickled.data["rank"]
            self.all_ranks[sock_uuid] = rank

        # Cancel the commands by uuid
        elif unpickled.type == "canceljob":
            uuids = unpickled.data["uuids"]
            if uuids:
                for id in uuids:
                    self.rem_cmds(self.get_cmd_by_uuid(id), JobStatus.CANCELLED.value)
        
        # Pause the commands by uuid
        elif unpickled.type == "pausejob":
            uuids = unpickled.data["uuids"]
            if uuids:
                for id in uuids.copy():
                    for cmd in self.commands:
                        if cmd.uuid == id:
                            cmd.status = JobStatus.PAUSED.value
                            # logger.info(f"Paused job {id}")
                            self.send_cmds_to_db()
                            uuids.remove(id)
                            break
                if len(uuids) > 0:
                    logger.spaces(f"SERVER: Could not pause jobs {uuids}")

        # Resume the commands by uuid
        elif unpickled.type == "resumejob":
            uuids = unpickled.data["uuids"]
            if uuids:
                for id in uuids.copy():
                    for cmd in self.commands:
                        if cmd.uuid == id:
                            cmd.status = JobStatus.INPROGRESS.value
                            # logger.info(f"Resumed job {id}")
                            self.send_cmds_to_db()
                            uuids.remove(id)
                            break
                if len(uuids) > 0:
                    logger.spaces(f"SERVER: Could not resume jobs {uuids}")


        elif unpickled.type == "donework":
            workid  = unpickled.data["workid"]
            result = unpickled.data["result"]
            cmd_uuid = unpickled.data["uuid"]
    
            # TODO use the CapoomWork class for Works and get rid of (cmd_uuid, workid) tuples
            if self.get_assigned_CapoomWork_by_cmduuid_workid(cmd_uuid, workid) is not None:

                
                # Remove from assigned
                # self.assigned = {k: v for k, v in self.assigned.items() if v != (cmd_uuid, workid)}
                self.rm_assigned_CapoomWork_by_cmd_id_and_work_id(cmd_uuid, workid)
                
                if self.get_cmd_by_uuid(cmd_uuid) is None:
                    logger.warning(f"Command with uuid {cmd_uuid} not found")
                    return
                    
                if result == True:
                    self.get_cmd_by_uuid(cmd_uuid).remaining.remove(workid)
                    # self.commands[0].remaining.remove(workid)
                    logger.debug(f"Work {cmd_uuid,workid} done, removed from remaining")
    
                # Error returned
                elif result == False:
                    pass
                self.send_cl_to_admins()
                self.send_cmds_to_db()
                
            else:
                # This should never happen
                logger.error("Work id not found in assigned workids list")

        # changing the priority of the command
        elif unpickled.type == "chagepriority":
            uuid = unpickled.data["uuid"]
            priority = unpickled.data["priority"]
            self.get_cmd_by_uuid(uuid).priority = priority
            self.sort_commands()
    

        elif unpickled.type == "getclients":
            self.send_cl_to_admins()

        elif unpickled.type == "getcommands":
            self.send_cmds_to_db()
        
        elif unpickled.type == "updatesocks":
            ucmd_uuids = unpickled.data["uuids"]
            if ucmd_uuids:
                for ucmd_uuid in ucmd_uuids:
                    self.update_cmd_socks(unpickled.data["socks"],ucmd_uuid)

        elif unpickled.type == "updateClients":
            logger.warning(f"Update command from admin => {ip}")
    
        elif unpickled.type == "backup_db":
            logger.warning(f"DB backup command from admin => {ip}")
            self.backup_db()

        logger.log(unpickled.logginglvl, unpickled.message)
     

    def get_cmd_by_uuid(self, uuid):
        for cmd in self.commands:
            if cmd.uuid == uuid:
                return cmd
        return None
       
    
    def handle_jobs(self, socket, cmd):
        
        if cmd.data["error_count"] > 9:
            logger.critical("Command failed 10 times, removing it")
            # self.rem_cmds(cmd, JobStatus.FAILED.value)
            cmd.status = JobStatus.FAILED.value
            return

        sock_uuid = self.get_sock_uuid(socket)

        if sock_uuid in [x.sock_uuid for x in self.assigned if x.sock_uuid == sock_uuid]:
            # Client disconnected during work
            if socket not in self.all_connections:
                self.remove_sock(socket, "Client disconnected during work")
                
                return
        elif self.all_ranks[sock_uuid] == ClientRanks.ADMIN.value:
            return
        
        # elif self.all_stats[sock_uuid] == "offline":
        #     return
        else:
            
            workid_to_assign = None
            
            if len(cmd.remaining) > 0:
                

                # Find the workid to assign
                # We have target command when we are in a render command. 
                # Target command is the command that we are rendering caches for
                
                target_cmd = None

                if cmd.type == "render":
                    
                    target_cmd = self.get_cmd_by_uuid(cmd.data["target_uuid"])

                    if target_cmd is not None:
                        if target_cmd in self.commands:
        
                            for workid in cmd.remaining:
                                if self.get_assigned_CapoomWork_by_cmduuid_workid(cmd.uuid, workid) not in self.assigned and workid not in target_cmd.remaining:
                                    workid_to_assign = workid
                                    break

                        else:
                            logger.error(f"Target command {target_cmd.uuid} not found")
                            self.rem_cmds(cmd, JobStatus.FAILED.value)

                            return
                    
                        
                
                else:
                    for workid in cmd.remaining:
                        if self.get_assigned_CapoomWork_by_cmduuid_workid(cmd.uuid, workid) not in self.assigned:
                            workid_to_assign = workid
                            break
                    
                    

                        
                ## Workid found, assign it
                
                # Assign the work
                if workid_to_assign != None:

                    if cmd.data["workids_tries"][workid_to_assign] > 3:
                        logger.critical(f"Work {cmd.uuid, workid_to_assign} failed 3 times, removing from remaining!")
                        cmd.remaining.remove(workid_to_assign)
                        self.send_cmds_to_db()
                        return

                    else:
                        self.assigned.append(CapoomWork(sock_uuid, cmd.uuid, workid_to_assign))
                        

                        datas = cmd.data.copy()
                        datas["workid"] = workid_to_assign
                        datas["uuid"] = cmd.uuid

                        cmd.data["workids_tries"][workid_to_assign] += 1
                        projectid = cmd.data["projectid"]
                        version = cmd.version

                        # Send the work to the client
                        socket.send(pickle.dumps(CapoomResponse(cmd.type,datas,"Create command from server")))

                        logger.info(f"Workid {workid_to_assign} of {projectid} w version {version} assigned to {socket.getpeername()[0]}")
                        return
                else:
                    # Something went wrong

                    if len(cmd.remaining) > 0 and len([x for x in self.assigned if x.cmd_uuid == cmd.uuid]) == len(cmd.remaining):
                        logger.debug("All workids are assigned, but not all workids are done")
                        return

                    elif len(cmd.remaining) > 0 and len([x for x in self.assigned if x.cmd_uuid == cmd.uuid]) == 0 and cmd.type == "render":
                        logger.debug("No workids are assigned, but not all workids are done, waiting for new cache to render")
                        # cmd.data["error_count"] += 1
                        return

                    else:
                        logger.warning("Workid to assign is None. Trying to assign work again")
                        cmd.data["error_count"] += 1
                        return

                    return
            else:
                # No work left, remove the command
                # self.rem_cmds(cmd, JobStatus.COMPLETED.value)
                
                cmd.status = JobStatus.COMPLETED.value
                self.send_cmds_to_db()
                return

   

    def update_cmd_socks(self,ips,job_uuid):

        cmd = self.get_cmd_by_uuid(job_uuid)
        cmd.sockets = []
        cmd.data["ips"] = []
        
        for ip in ips:
            sock = self.get_sock_from_ip(ip)
            if sock not in cmd.sockets:
                cmd.sockets.append(sock)
                cmd.data["ips"].append(ip)
                logger.info(f"Added {ip} to {job_uuid}")
                self.send_cmds_to_db()

    def backup_db(self):     
        while True:
            try:
                logger.info("Backing up database")

                backup_date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
               
                subprocess.Popen(f"pg_dump -U postgres -d opusdb -f P:/pipeline/standalone/db_backup/backup_{backup_date}.sql")
            except Exception as e:
                logger.error(f"Error while backing up db: {e}")

            time.sleep(86400)


    # This is where we read and write data
    def communication(self):
        while True:
            for conn in self.all_connections:
                try:
                    conn.settimeout(self.timeout)
                    data = conn.recv(self.max_data)

                    if data:
                        actual_data = pickle.loads(data)
                        
                        #Read commands
                        if isinstance(actual_data, CapoomCommand):
                            self.read_cmds(actual_data)
                    
                        # Read responses
                        elif isinstance(actual_data, CapoomResponse):
                            self.read_responses(actual_data, conn)
                        
                        # Invalid data
                        else:
                            logger.warning(f"invalid data {data} from {conn.getpeername()[0]}")
                            # self.remove_sock(conn,"Graceful")
                            # self.send_cl_to_admins()
                            pass       

                except socket.timeout:
                    pass

                # Disconnected forcibly
                except socket.error as e:
                    self.remove_sock(conn,"Forcibily")
                    self.send_cl_to_admins()
                    

                # Other exceptions
                except Exception:
                    
                    sys.excepthook(*sys.exc_info())
                    pass
            
            #-- DONE READING DATA


            # Check if we need to send commands
            if len(self.commands) == 0:
                continue
            else:

                # Handle the commands
                for conn in self.all_connections:
                    
                    try:
                        if self.commands:
                            
                            for cmd_index, cmd in enumerate(self.commands):
                                if cmd.status == JobStatus.PAUSED.value or cmd.status == JobStatus.FAILED.value or cmd.status == JobStatus.COMPLETED.value or cmd.status == JobStatus.NOTSTARTED.value:
                                    continue
                                if conn in self.commands[cmd_index].sockets:  
                                    self.handle_jobs(conn, cmd)


                    except socket.error as e:
                        logger.error(f'error while sending commands {e}')
                        logger.error(f"{conn.getpeername()[0]} might not recieved command")
                    except Exception as e:
                        sys.excepthook(*sys.exc_info())
                        pass




if __name__ == "__main__":

    server = None
    
    try:
        server = CapoomServer()
    except KeyError as e:
        logger.error(f"Invalid File: {e.args[0]} is not in the JSON file")
    
    if server is not None:
        
        conn_handler = threading.Thread(None, server.accepting_connections, "ConnectionHandler")
        conn_handler.start()

        data_handler = threading.Thread(None, server.communication, "DataHandler")
        data_handler.start()

        db_backup = threading.Thread(None, server.backup_db, "DBBackup")
        db_backup.start()
        
        

    else:
        logger.error("Server could not be started!")


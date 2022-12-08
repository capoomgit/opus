
# STD LIBS
import os
import socket, threading, json, pickle, sys, time
import subprocess
import configparser


from runhda_dev import init_creation, create_structure
from server_utils import CapoomResponse
from render import render_smth
from get_credentials import get_credentials
from consts import ClientRanks, ClientStatus
import hou
from stage import stage_usd

import psycopg2
import psycopg2.extras

SAVE_PATH = "P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{version}/Objects/"
STANDALONE_PATH = "P:/pipeline/standalone/client/"
VERSION_PATH = "P:/pipeline/standalone/version.ini"

import logging
from logger import setup_logger
logger = setup_logger(f"{socket.gethostname()}_slave.log")

creds = get_credentials()
print(creds)
class CapoomSlave(threading.Thread):
    def __init__(self, settings):
        # Threading
        threading.Thread.__init__(self)
        self.running = True

        # Other
        self.settings = settings
        self.addr = creds["server_ip"]
        print(self.addr)
        self.port = creds["server_port"]
        self.buffsize = 16384000

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.desired_status = ClientStatus.AVAILABLE.value

        # We store the responses we want to send here and periodically send them
        # to the server, reason why we do this is since the server is not async sometimes it misses responses
        self.responses_to_send = []

    def connect(self):
        logger.info("Trying to connect to server")
        ret = self.server_socket.connect_ex((self.addr, self.port))
        # read version
        with open("version.txt", "r") as f:
            self.cur_version = f.read()
            logger.info(f"Current version is {self.cur_version}")

        
        if ret != 0:
            logger.error("Couldn't connect to server")
            self.reconnect()
            return
        logger.info("Successfully connected to server")
    
    def communicate_with_server(self):
        while self.running:
            time.sleep(1)
            print("Checking responses")
            print("Response length is", len(self.responses_to_send))

            # Send responses
            if len(self.responses_to_send) > 0:
                for response in self.responses_to_send:
                    logger.info(f"Sending response to server: {response.message}")
                    self.server_socket.send(pickle.dumps(response))
                    time.sleep(3)
                self.responses_to_send = []
    
    def run(self):
        """ Executes client main thread """
        self.set_rank(ClientRanks.CLIENT.value)
        self.set_status(self.desired_status)

        while self.running:
            try:
                # Ping server
                data = self.server_socket.recv(self.buffsize)
                # Check if there is any data
                if data:
                    actual_data = pickle.loads(data)
                    if isinstance(actual_data, CapoomResponse):
                        
                        self.set_status(ClientStatus.BUSY.value)
                        # Handling commands
                        if actual_data.type == "create_structure":
                            job_uuid = actual_data.data["uuid"]
                            do_stage = actual_data.data["stage"]
                            do_render = actual_data.data["render"]


                            cache_result, stage_result, render_result = None, None, None


                            try:
                                cache_result = self.create(actual_data)
                            except Exception as e:
                                logger.error(f"Error while creating structure: {e}")
                                cache_result = False
                            if do_stage:
                                stage_result = self.stage(actual_data)
                            else:
                                stage_result = True

                            if do_render:
                                render_result = self.render(actual_data)
                            else:
                                render_result = True

                            if any([cache_result, stage_result, render_result]):
                                result = CapoomResponse("create_structure",
                                                        {"result":True},
                                                        f"Created structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.INFO)
                            elif not cache_result:
                                result = CapoomResponse("create_structure",
                                                        {"result":False},
                                                        f"Error while creating structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.ERROR)
                            elif not stage_result:
                                result = CapoomResponse("create_structure",
                                                        {"result":False},
                                                        f"Error while staging structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.ERROR)
                            elif not render_result:
                                result = CapoomResponse("create_structure",
                                                        {"result":False},
                                                        f"Error while rendering structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.ERROR)



                        if actual_data.type == "render":
                            if actual_data.data["do_stage"]:
                                stage_result = self.stage(actual_data)
                            else:
                                stage_result = True

                            render_result = self.render(actual_data)

                            if any([stage_result, render_result]):
                                result = CapoomResponse("render",
                                                        {"result":True},
                                                        f"Rendered structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.INFO)
                            elif not stage_result:
                                result = CapoomResponse("render",
                                                        {"result":False},
                                                        f"Error while staging structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.ERROR)
                            elif not render_result:
                                result = CapoomResponse("render",
                                                        {"result":False},
                                                        f"Error while rendering structure {socket.gethostname()} with Job UUID {job_uuid}", logginglvl=logging.ERROR)

                    self.responses_to_send.append(result)
                    self.set_status(self.desired_status)

            except BlockingIOError as e:
                pass
            except socket.error as e:
                logger.critical(f"{socket.gethostname()} lost connection with the server, trying to reconnect, reason: {e}")
                self.reconnect()

    # TODO actually make this work for objects aswell
    def create(self, actual_data : CapoomResponse) -> bool:
        """ Creates the structure/object from given data\n
        `actual_data` CapoomResponse object that contains needed information\n
        `return` CapoomResponse object  with result, workid and jobs uuid"""
        structure = actual_data.data["structure"]
        project_id = actual_data.data["projectid"]
        work_id = actual_data.data["workid"]
        version = actual_data.data["version"]
        # job_uuid = actual_data.data["uuid"]

        # Render settings
        logger.info(f"Creating {structure} for project {project_id} and work {work_id} for version {version}")

        init_creation()
        try:
            cache_result = create_structure(structure, project_id, work_id, version)
        except Exception as e:
            logger.error(f"Failed to create {structure} for project {project_id} and work {work_id} for version {version}, reason: {e}")
            cache_result = False
        return cache_result

        # ref_version = str(version).zfill(4)
        # merge_file = f"P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{ref_version}/Objects/Merged/Merged_{project_id}_{work_id}_{ref_version}.bgeo.sc"

        # if to_send.data["result"]:
        #     # Save the workid to finished.txt
        #     with open(SAVE_PATH.format(structure=structure, project_id=project_id, version=str(version).zfill(4)) + "finished.txt", "a") as f:
        #         print()
        #         f.write(f"{work_id}\n")

    def stage(self, actual_data : CapoomResponse) -> bool:
        """ Stages the given cache so we can render using USD pipeline
        `actual_data` CapoomResponse object that contains needed information\n
        `return` Result of the render"""

        structure = actual_data.data["structure"]
        project_id = actual_data.data["projectid"]
        work_id = actual_data.data["workid"]
        version = actual_data.data["version"]
        job_uuid = actual_data.data["uuid"]
        ref_version = str(version).zfill(4)

        # TODO implement this
        frame_count = 10

        merge_file = f"P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{ref_version}/Merged/Merged_{project_id}_{work_id}_{ref_version}.bgeo.sc"
        stage_save_path = f"P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{ref_version}/Staged/"

        stage_result = stage_usd(merge_file, stage_save_path, project_id, work_id, ref_version, frame_count)

        if stage_result is True:
            return True
        else:
            logger.error(f"Failed to stage {structure} for project {project_id} and work {work_id} for version {version}, UUID: {job_uuid}\nReason: {stage_result}")
            return False

    def render(self, actual_data : CapoomResponse) -> bool:
        """ Renders the given file\n
        `actual_data` CapoomResponse object that contains needed information\n
        `return` Result of the render"""

        structure = actual_data.data["structure"]
        project_id = actual_data.data["projectid"]
        work_id = actual_data.data["workid"]
        version = actual_data.data["version"]
        job_uuid = actual_data.data["uuid"]
        ref_version = str(version).zfill(4)

        render_engine = actual_data.data["render_engine"]
        frame_count = actual_data.data["frame_count"]


        # TODO implement other engines again
        if render_engine != "omniverse":
            return CapoomResponse("donework",
                                {"result":False, "workid":work_id, "uuid":job_uuid},
                                f"Engines other than omniverse are not supported",
                                logginglvl=logging.ERROR)


        stage_file = f"P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{ref_version}/Staged/Staged_{project_id}_{work_id}_{ref_version}.usd"
        render_save_path = f"P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{ref_version}/Rendered/Render_{project_id}_v{ref_version}"


        render_result = render_smth(stage_file, render_save_path, project_id, work_id, version, frame_count)

        if render_result is True:
            return True
        else:
            logger.error(f"Failed to render {structure} for project {project_id} and work {work_id} for version {version}, UUID: {job_uuid}\nReason: {render_result}")
            return False


        # to_send = None

        # if render_result:
        #     to_send = CapoomResponse("donework",
        #                             {"result":True, "workid":work_id, "uuid":job_uuid},
        #                             f"Successfully rendered {structure} for project {project_id} and work {work_id} for version {version}, UUID: {job_uuid}",
        #                             logginglvl=logging.INFO)
        # else:
        #     to_send = CapoomResponse("donework",
        #                             {"result":False, "workid":work_id, "uuid":job_uuid},
        #                             f"Failed to render {structure} for project {project_id} and work {work_id} for version {version}, UUID: {job_uuid}",
        #                             logginglvl=logging.ERROR)


        return stage_result


    def check_do_update(self):
        """ Checks if the server should update itself\n
            This is done by checking `version.ini` on the standalone path on capoom_storage"""
        while True:
            time.sleep(5)
            try:
                config = configparser.ConfigParser()
                version_file = config.read(VERSION_PATH)

                if version_file:
                    hostname=socket.gethostname()
                    IPAddr=socket.gethostbyname(hostname)
                    
                    indiv_update = config.getboolean("IndividualUpdates", str(IPAddr))
                    if indiv_update:
                        logger.warning(f"Admin requested update on this computer")
                        config.set("IndividualUpdates", str(IPAddr), 'false')
                        with open(VERSION_PATH, 'w') as configfile:
                            config.write(configfile)

                        subprocess.Popen('capoom updater.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
                        self.stop_connection()
            
            except Exception as e:
                    logger.error(f"Failed to check for updates, reason: {e}")
                    pass
    
    def reconnect(self):
        """ Reconnects to the server if the connection is lost"""
        while True:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ret = self.server_socket.connect_ex((self.addr, self.port))
            if ret != 0:
                logger.warning("Couldn't reconnect to server")
                time.sleep(5)
                continue

            logger.info("Successfully reconnected to server")
            self.set_rank(ClientRanks.CLIENT.value)
            self.set_status(self.desired_status)
            break

    def stop_connection(self):
        os._exit(1)

    def set_status(self, status):
        self.responses_to_send.append(CapoomResponse("status", {"status":status}, f"{socket.gethostname()} is {status}", logginglvl=logging.INFO))

    def set_rank(self, rank):
        self.responses_to_send.append(CapoomResponse("rank", {"rank":rank}, f"{socket.gethostname()} is a {rank}", logginglvl=logging.INFO))

    def set_desired_status(self, status):
        self.desired_status = status
        self.responses_to_send.append(CapoomResponse("status", {"status":status}, f"{socket.gethostname()} is {status}", logginglvl=logging.INFO))

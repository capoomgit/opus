import threading
import json
import socket
import pickle
import os, sys
import time
import logging
import configparser

from server_utils import CapoomCommand
from server_utils import CapoomResponse

from consts import ClientRanks, ClientStatus
from logger import setup_logger

STANDALONE_PATH = "P:/pipeline/standalone/client/"
VERSION_PATH = "P:/pipeline/standalone/version.ini"


logger = setup_logger(f"{socket.gethostname()}_admin.log")
# logger.basicConfig(filename=f"P:/pipeline/standalone_dev/logs/{socket.gethostname()}_admin_log.txt", format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logger.DEBUG)
# logger.getLogger().addHandler(logger.StreamHandler())

# TODO integrate QT
class CapoomAdminClient(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.running = True
        self.connected = False
        self.commands = []

        self.all_clients = {}

        
        self.server_cmds = None
        
        self.buffsize = 1638400
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logpath = f"P:/pipeline/standalone_dev/logs/{socket.gethostname()}_admin_log.txt"

        logger.info(f"Trying to connect to {self.ip}:{self.port}")
        ret = self.server_socket.connect_ex((self.ip, self.port))
        if ret != 0:
            logger.error("Couldn't connect to server")
            return
        logger.info(f"Succesfully connected to {self.ip}:{self.port}")
        self.connected = True


    def run(self):
        """ Admin Client main thread """

        #Connected
        # self.server_socket.send(pickle.dumps(CapoomResponse("rank", {"rank":"admin"}, f"{socket.gethostname()} is an admin")))
        self.set_rank(ClientRanks.ADMIN.value)
        time.sleep(1)
        self.server_socket.send(pickle.dumps(CapoomResponse("getclients", {"getclients":"all"}, f"Get all clients")))

        while self.running:
            # Send list of the all comments (has to be ordered)
            if len(self.commands) != 0:
                self.server_socket.send(pickle.dumps(self.commands[0]))
                self.commands.clear()
            #Get data
            try:
                self.server_socket.settimeout(1)
                data = self.server_socket.recv(self.buffsize)
                #Check if there is any data
                if data:
                    actual_data = pickle.loads(data)

                    # TODO change this to CapoomResponse
                    if isinstance(actual_data,tuple):
                        #Get Client Lists
                        if actual_data[0] == "clients":
                            self.all_clients = actual_data[1]
                            logger.info(f'Received clients: {actual_data[1]}')
            except socket.timeout:
                pass
            except Exception as e:
                logger.error(f"Error: {e}")
                # self.running = False
                self.connected = False
                self.reconnect()

    
    def stop_connection(self):
        """ Stops the connection """
        self.running = False
        logger.info("Disconnected from Server")

    # TODO change this to work with all structures
    def create_structure(self, selected, data, count, version, status, assigner, priority):
        """ Sends create structure command to the server to be executed from clients"""
        self.commands.append(CapoomCommand(selected, data, "create_structure", count, version, status, assigner, priority=priority))
    
    def render(self, selected, data, count, version, status, assigner, priority):
        """ Sends render command to the server to be executed from clients"""
        self.commands.append(CapoomCommand(selected, data, "render", count, version, status, assigner, priority=priority))
    
    def send_new_workers(self, workers, jobuuids, jobinfos):
        self.commands.append(CapoomResponse("updatesocks",{"socks":workers, "uuids":jobuuids}, f"{socket.gethostname()} has updated the jobs below with {workers} joining work force: {jobinfos}", logginglvl=logging.INFO))

    def cancel_job(self,jobuuids,jobinfos):
        """Cancels the selected job"""
        self.commands.append(CapoomResponse("canceljob",{"uuids":jobuuids}, f"{socket.gethostname()} STOPPED jobs: {jobinfos}", logginglvl=logging.SPACES))
    
    def resume_job(self,jobuuids,jobinfos):
        """Resumes the selected job"""
        self.commands.append(CapoomResponse("resumejob",{"uuids":jobuuids}, f"{socket.gethostname()} RESUMED jobs: {jobinfos}", logginglvl=logging.SPACES))

    def pause_job(self,jobuuids,jobinfos):
        """Pauses the selected job"""
        self.commands.append(CapoomResponse("pausejob",{"uuids":jobuuids}, f"{socket.gethostname()} PAUSED jobs: {jobinfos}", logginglvl=logging.SPACES))

    def update_clients(self):
        # self.commands.append(CapoomResponse("updateClients", {}, "Update clients"))
        config = configparser.ConfigParser()
        version_file = config.read(VERSION_PATH)

        if version_file:

            all_computers = dict(config.items("IndividualUpdates"))
            for computer in all_computers.keys():
                logging.warning(f"{socket.gethostname()} is updating clients")
                config.set("IndividualUpdates", computer, 'true')

            with open(VERSION_PATH, 'w') as configfile:
                config.write(configfile)

    def set_rank(self, rank):
            self.server_socket.send(pickle.dumps(CapoomResponse("rank", {"rank":rank}, f"{socket.gethostname()} is a {rank}", logginglvl=logging.INFO)))

    def get_clients_from_server(self):
        self.commands.append(CapoomResponse("getclients", {}, "Get clients"))

    def reconnect(self):
        logger.critical(f"{socket.gethostname()} lost connection with the server!")
        while True:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ret = self.server_socket.connect_ex((self.ip, self.port))
            if ret != 0:
                logger.warning("Couldn't connect to server")
                time.sleep(5)
                continue

            logger.info("Successfully connected to server")
            self.set_rank(ClientRanks.ADMIN.value)
            self.connected = True
            time.sleep(2)
            break

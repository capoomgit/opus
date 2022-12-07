from uuid import uuid4
import logging
class CapoomResponse:
    def __init__(self, type, data, message, logginglvl = logging.DEBUG):
        self.type = type
        self.data = data
        self.message = message
        self.logginglvl = logginglvl


class CapoomCommand:
    def __init__(self, sockets, data, type, count, version, status, assigner, priority=50):
        self.sockets = sockets
        self.data = data
        self.type = type
        self.count = count
        self.remaining = []
        self.version = version
        self.status = status
        self.assigner = assigner
        self.uuid = uuid4()
        self.priority = priority

        # Sanity check
        self.initalized_remaining = False

    def init_remaining(self):
        """Initializes the remaining list with the count of the command"""
        if not self.initalized_remaining:
            self.remaining = [x for x in range(self.count)]
            self.initalized_remaining = True
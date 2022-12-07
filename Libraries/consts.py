from enum import Enum


class JobStatus(Enum):
    NOTSTARTED = "Not Started"
    INPROGRESS = "In Progress"
    CANCELLED = "Cancelled"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    FAILED = "Failed"

class ClientStatus(Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    OFFLINE = "Offline"
    DND = "DnD"

class ClientRanks(Enum):
    ADMIN = "Admin"
    CLIENT = "Client"
from PySide2 import QtWidgets
import toolbox
from database import Database
import panel_utils
from imp import reload
import hda_register
reload(toolbox)
reload(panel_utils)
reload(hda_register)
#initialise the database
from get_credentials import get_credentials

credentials = get_credentials()
dbname = credentials["db_name"]
user = credentials["db_user"]
password = credentials["db_password"]
host = credentials["db_host"]
port = credentials["db_port"]

Database.initialise(user=user, password=password, database=dbname, host=host)
def createInterface():
     
     root = toolbox.create_toolbox()
     return root
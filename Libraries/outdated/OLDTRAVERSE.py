# STD libs
import random, json, os    

# libs
import psycopg2
import psycopg2.extras
import hou
from get_credentials import get_credentials

credentials = get_credentials()
dbname = credentials["db_name"]
user = credentials["db_user"]
password = credentials["db_password"]
host = credentials["db_host"]
port = credentials["db_port"]


con = psycopg2.connect(f"dbname={dbname} user={user} password={password} host={host}, port={port}")
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_ends(sort=True):

    GETEND = """SELECT * FROM public.mocktable WHERE "end" = %s"""

    if sort:
        cur.execute(GETEND, (True,))
        ends = cur.fetchall()
        ends = sorted(ends, key=lambda k: k['creation_order'])
    return ends


def cast_parm(val, parmtype : str):
    """ Casts the value of first string into type of second string """
    try:
        if parmtype.lower() == "float":
            return float(val)
        elif parmtype.lower() == "int":
            return int(val)
    except Exception as e:
        return e

# TODO ask berkay how the fuck are we supposed to traverse for all inputs lmao
def traverse(node, cur_path, parentid):
    cur_path.append(node["id"])
    if node["start"] == True:
        return cur_path

    if node["parents_" + str(parentid)] != None:
        if len(node["parents_" + str(parentid)]) > 1:
            # TODO weighted randomness
            rand_parent = node["parents_" + str(parentid)][random.randint(0, len(node["parents_" + str(parentid)]) - 1)]
            print("Multiple choices, chose:", rand_parent)
            select_parent = "SELECT * FROM public.mocktable WHERE id = %s"
            cur.execute(select_parent, (rand_parent,))
            parent_node = cur.fetchone()
            return traverse(parent_node, cur_path, parentid)

        elif len(node["parents_" + str(parentid)]) == 1:
            select_parent = "SELECT * FROM public.mocktable WHERE id = %s"
            cur.execute(select_parent, (node["parents_" + str(parentid)][0],))
            parent_node = cur.fetchone()
            print("Single path to:", node["parents_" + str(parentid)][0])
            return traverse(parent_node, cur_path, parentid)
        else:
            raise Exception("No parents found for node", node["id"], "\n this node is probably not connected to the graph")


def create():
    # migrate to slave
    all_paths = []
    for i, end in enumerate(get_ends()):
        paths = []
        print("Traversing", end["id"], "with creation order", end["creation_order"])

        for parent in range(0, 4):
            path = traverse(end, [], parent)
            paths.extend(path if path is not None else [])
        merge = set(paths)
        all_paths.append(merge)


def get_node(id):
    cur.execute("SELECT * FROM public.mocktable WHERE id = %s", (id,))
    return cur.fetchone()


if __name__ == "__main__":
    create()
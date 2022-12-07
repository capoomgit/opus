import psycopg2
import psycopg2.extras
from random import randint

GETEND = """SELECT * FROM public.mocktable WHERE "end" = %s"""
from get_credentials import get_credentials

credentials = get_credentials()
dbname = credentials["db_name"]
user = credentials["db_user"]
password = credentials["db_password"]
host = credentials["db_host"]
port = credentials["db_port"]


con = psycopg2.connect(f"dbname={dbname} user={user} password={password} host={host}, port={port}")
db_cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)



cur.execute(GETEND, (True,))
ends = cur.fetchall()

# TODO ask berkay how the fuck are we supposed to traverse for all inputs lmao

def traverse(node, cur_path, parentid):
    cur_path.append(node["id"])
    if node["start"] == True:
        return cur_path

    if node["parents_" + str(parentid)] != None:
        if len(node["parents_" + str(parentid)]) > 1:
            # TODO weighted randomness
            rand_parent = node["parents_" + str(parentid)][randint(0, len(node["parents_" + str(parentid)]) - 1)]
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


def create():
    # migrate to slave
    all_paths = []
    for i, end in enumerate(ends):
        paths = []
        for parent in range(0, 4):
            path = traverse(end, [], parent)
            paths.extend(path if path is not None else [])
        merge = set(paths)
        all_paths.append(merge)
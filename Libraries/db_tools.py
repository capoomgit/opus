import psycopg2
import psycopg2.extras
from get_credentials import get_credentials

credentials = get_credentials()
dbname = credentials["db_name"]
user = credentials["db_user"]
password = credentials["db_password"]
host = credentials["db_host"]
port = credentials["db_port"]


con = psycopg2.connect(f"dbname={dbname} user={user} password={password} host={host}, port={port}")
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)



def delete_hda(hda_id):
    cur.execute("""DELETE FROM "Hdas" WHERE id = %s""",(hda_id,))
    con.commit()

    cur.execute("""SELECT * FROM "Paths" """)
    path_hdas = cur.fetchall()
    for path_hda in path_hdas:
        if hda_id in path_hda["hdas"]:
            path_hda["hdas"].remove(hda_id)
            cur.execute("""UPDATE "Paths" SET hdas = %s WHERE id = %s""",(path_hda["hdas"],path_hda["id"]))
            
            con.commit()




delete_hda(27)
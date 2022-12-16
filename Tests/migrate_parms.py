import psycopg2
import psycopg2.extras
from get_credentials import get_credentials

credentials = get_credentials()
conn = psycopg2.connect(f"dbname={credentials['db_name']} user={credentials['db_user']} host={credentials['db_host']} password={credentials['db_password']}")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cur.execute("""SELECT * FROM "Hdas" """)
hdas = cur.fetchall()

for hda in hdas:
    # Check if we already have this hda_id and version in the parameters table
    cur.execute("""SELECT * FROM "Parameters" WHERE hda_id = %s AND hda_version = %s""", (hda["hda_id"], hda["hda_version"]))
    if cur.fetchone():
        continue

    # Insert the parameter related values into parmeter table
    cur.execute(""" INSERT INTO "Parameters" (hda_id, hda_version, parm_name, parm_min, parm_max, parm_default, parm_type, parm_override) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
    (hda["hda_id"], hda["hda_version"], hda["parm_names"], hda["parm_mins"], hda["parm_maxes"], hda["parm_defaults"], hda["parm_types"], hda["parm_override_mode"]))
    conn.commit()
    print("Inserted parameters for hda_id: ", hda["hda_id"], "hda_version: ", hda["hda_version"])
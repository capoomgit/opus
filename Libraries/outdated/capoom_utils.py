import json



def save_hip(hou, path, name):
    print("Saved hip")
    hou.hipFile.save(file_name=f"{path}/{name}.hiplc",save_to_recent_files=0)
    pass

# TODO integrate this into every client
def get_settings():
    read_file = open("P:/pipeline/standalone/settings.json", "r")
    from_file = json.load(read_file)
    read_file.close()
    return from_file

def filecache(geo,input_geo,path,workid):
    filecache = geo.createNode('filecache')
    filecache.setInput(0,input_geo)
    filecache.moveToGoodPosition(move_inputs=False)
    filecache.parm('filemethod').set(1)
    filecache.parm('trange').set(0)
    filecache.parm('file').set(f"{path}/{workid}.bgeo.sc")
    filecache.parm('execute').pressButton()

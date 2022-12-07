import hou
import random
import capoom_utils
import traceback
import json
import os
def cast_parm(val, parmtype : str):
    """ Casts the value of first string into type of second string """
    try:
        if parmtype.lower() == "float":
            return float(val)
        elif parmtype.lower() == "int":
            return int(val)
    except Exception as e:
        return e


def callHDA(folder, projectid, workid, hdaname, version, dependencies, parms, parmmins, parmmaxes, parmtypes, parmmode, defaults, dependent_out):
    # Randomize all the parm values that need to be randomized 
    # and set all the values that need to be set
    try:
        all_param_vals = {}
        cur_seed = projectid + workid
        rand_obj = random.Random(cur_seed)
        

        for i, parm in enumerate(parms):
            if parmmode[i] == False:
                rand_obj.seed(cur_seed)
                actualmin = parmmins[i]
                actualmax = parmmaxes[i]
                actualval = cast_parm(rand_obj.uniform(actualmin, actualmax), parmtypes[i])
                all_param_vals[parm] = actualval
                cur_seed+=1
            else:
                all_param_vals[parm] = cast_parm(defaults[i], parmtypes[i])
        
        
        # Clear the scene.
        hou.hipFile.clear(suppress_save_prompt=1)

        obj = hou.node("/obj")
        geo = obj.createNode("geo", f"{hdaname}_{projectid}_{workid}")
        
        # Create the current node
        actual_node = geo.createNode(f"capoom::dev::{hdaname}")

        if len(dependencies) != 0:
            for i, dependent in enumerate(dependencies):
                filecache = geo.createNode('filecache')
                filecache.moveToGoodPosition(move_inputs=False)
                filecache.parm('loadfromdisk').set(1)
                filecache.parm('filemethod').set(1)
                filecache.parm('trange').set(0)
                filecache.parm('file').set(f"{folder}/{projectid}/{dependent}_{projectid}/Out_{str(dependent_out[i])}/{dependent}_{projectid}_{workid}.bgeo.sc")
                
                actual_node.setInput(i, filecache)


        for i, parm in enumerate(all_param_vals):
            actual_node.parm(parms[i]).set(all_param_vals[parm])

        path = f"{folder}/{projectid}/{hdaname}_{projectid}/"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(f"{path}\\parms_{hdaname}_{projectid}_{workid}.json", "w") as f:
            json.dump(all_param_vals, f, indent=4)

        for i in range(len(actual_node.outputConnectors())):
                filecache2 = geo.createNode('filecache')
                filecache2.moveToGoodPosition(move_inputs=False)
                filecache2.parm('loadfromdisk').set(1)
                filecache2.parm('filemethod').set(1)
                filecache2.parm('trange').set(0)
                filecache2.parm('file').set(f"{folder}/{projectid}/{hdaname}_{projectid}/Out_{str(i)}/{hdaname}_{projectid}_{workid}.bgeo.sc")
                
                filecache2.setInput(0, actual_node, i)
                filecache2.parm('execute').pressButton()
        # capoom_utils.save_hip(hou, f"{folder}/{projectid}/{hdaname}/", workid)
        # Successfully ran hda


        return True
    
    except Exception as e:
        traceback.print_exc()
        return e

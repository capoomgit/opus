import psycopg2
import psycopg2.extras
import random
import sys,os
import json
import collections
from get_credentials import get_credentials

# import logging
# logging.basicConfig(filename=f"C:/Users/capoom/Documents/Arda/capoom_job_manager/libs/runhda_log.txt", format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler())

try:
    os.add_dll_directory("C:\\Program Files\\Side Effects Software\\Houdini 19.5.368\\bin")
except Exception:
    runhda_logger.critical("DLL directory could not be added")
    sys.exit()

import hou


SAVE_PATH = "P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{version}/Objects/"
MERGE_PATH = "P:/pipeline/standalone_dev/saved/{structure}/Project_{project_id}_v{version}/Merged/"
# SAVE_PATH = "P:/pipeline/standalone_dev/saved/{project_id}/Objects/"
CACHE_NAME = "{Object}/{Object}_{project_id}_{work_id}_Out_{Out}_ID_{id}"


GET_STRUCT_BY_NAME = """SELECT * FROM "Structures" WHERE structure_name = %s"""
GET_OBJECT_BY_ID = """SELECT * FROM "Objects" WHERE obj_id = %s"""
GET_OBJECT_BY_NAME = """SELECT * FROM "Objects" WHERE obj_name = %s"""
GET_COMPS_BY_ID = """SELECT * FROM "Components" WHERE component_id = %s"""
GET_PATHS_BY_ID = """SELECT * FROM "Paths" WHERE path_id = %s"""
GET_HDA_BY_ID = """SELECT * FROM "Hdas" WHERE hda_id = %s"""
GET_MULTIPLE_OBJECTS ="""SELECT * FROM "Objects" WHERE needed_data_for_multiple_objs NOTNULL"""

# Passing the logger from slave to here
runhda_logger = None
def init_logger(logger):
    global runhda_logger
    runhda_logger = logger
    runhda_logger.info("Runhda logger initialized")

def create_structure(structname, project_id, work_id, version):
    # Format XXXX
    version = str(version).zfill(4)

    # TODO remove count, instead use workid
    cur.execute(GET_STRUCT_BY_NAME, (structname,))
    structure = cur.fetchone()

    runhda_logger.info(f'Creating structure {structure["structure_name"]}')

    object_ids = structure["obj_ids"]
    obj_creation_results = []

    for obj_id in object_ids:
        cur.execute(GET_OBJECT_BY_ID, (obj_id,))
        obj = cur.fetchone()

        if obj in multiples:
            # We need to get rid of duplicates
            obj_styles = set(all_styles[obj["obj_name"]])
            for style_counter, obj_style in enumerate(obj_styles):
                result = create_object(obj_id, project_id, work_id, version, parent_structure=structname, style=obj_style, id=style_counter)
                obj_creation_results.append(result)

            create_placer(project_id, work_id, version, structname, obj["obj_name"], len(obj_styles))
        else:
            result = create_object(obj_id, project_id, work_id, version, parent_structure=structname)
            obj_creation_results.append(result)

    merge_objects_of_structure(project_id, work_id, version, parent_structure=structname)

    if all(obj_creation_results):
        runhda_logger.info("Structure created successfully")
        return True
    else:
        runhda_logger.info("Structure created but it has failed objects")
        return False
    # do stuff with cache_name


# TODO handle the save path errors that raises when we dont have a parent structure

def create_object(obj_id, project_id, work_id, version, parent_structure="Standalone", style=None, id=0, prediction_parms={}):
    try:
        cur.execute(GET_OBJECT_BY_ID, (obj_id,))
        obj = cur.fetchone()
        runhda_logger.info(f'Creating object {obj["obj_name"]}')


        # we can rename this after
        dependent_objs_ids = obj["dependent_obj_ids"]
        dependent_objs_outs = obj["dependent_obj_outs"]

        hou.hipFile.clear(suppress_save_prompt=1)
        houobj = hou.node("/obj")
        hougeo = houobj.createNode("geo")

        global obj_parms
        obj_parms = collections.defaultdict(dict)
        first_hda = None
        previous_layer_last_hda = None
        last_layer_last_hda = None
        # First we create our layers since this process is the same if we have dependencies or not
        layer_ids = obj["component_ids"]
        for i, layer_id in enumerate(layer_ids):
            cur.execute(GET_COMPS_BY_ID, (layer_id,))
            layer = cur.fetchone()

            # TODO move this into "HDA Template"
            layer_can_skip = layer["can_skip"]
            layer_skip_chance = layer["skip_chance"]

            # If the input is coming from ai we need to place each layer because we dont know which one will be used
            if not prediction_parms:
                layer_skip_random = random.random()
                if layer_can_skip and layer_skip_chance > layer_skip_random:
                    continue
            
            # TODO It is unclear if the hda is classified by AI, discuss it further
            # If it is classified, you just need to get the predicted path instead of randomly choosing one
            paths = []
            for path_id in layer["path_ids"]:
                cur.execute(GET_PATHS_BY_ID, (path_id,))
                path = cur.fetchone()
                paths.append(path)
            
            runhda_logger.debug(f"All paths {paths}")
            sel_path = random.choice(paths)
            runhda_logger.info(f"Selected paths {sel_path}")


            for j, hda_id in enumerate(sel_path["hda_ids"]):
                cur.execute(GET_HDA_BY_ID, (hda_id,))
                db_hda = cur.fetchone()

                seed = project_id + work_id + 5

                hda = None

                # This is a special hardcoded case,
                # we sometimes use nulls to get caches of outputs of some object as a seperate object by itself
                # (i.e WallFromPorch)
                if db_hda["hda_name"] == "Null":
                    hda=hougeo.createNode("null")
                else:
                    hda = place_hda(db_hda, hougeo)


                if i == j == 0:
                    first_hda = hda
                    if dependent_objs_ids and dependent_objs_outs:
                    # This lists indices are the input number of our first hda of this object
                        file_caches = []
                        # We have dependencies
                        for dep_i, dep_id in enumerate(dependent_objs_ids):
                            cur.execute(GET_OBJECT_BY_ID, (dep_id,))
                            dep_obj = cur.fetchone()

                            # Place the filecache
                            first_hda_in_fc = hougeo.createNode("filecache")

                            if dep_id == -1:
                                # TODO make the house part more generic
                                filepath = str(MERGE_PATH.format(project_id=project_id, version=version, structure="House") + f"/Merged_{project_id}_{work_id}_{version}.bgeo.sc")
                            else:
                                filepath = str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=dep_obj["obj_name"], project_id=project_id, work_id=work_id, Out=dependent_objs_outs[dep_i], id=0)+ ".bgeo.sc")
                            first_hda_in_fc.parm('loadfromdisk').set(1)
                            first_hda_in_fc.parm("file").set(filepath)
                            first_hda_in_fc.parm("filemethod").set(1)
                            first_hda_in_fc.parm("trange").set(0)
                            file_caches.append(first_hda_in_fc)

                        for input_i, fc in enumerate(file_caches):
                            first_hda.setInput(input_i, fc, 0)

                # Connect our previous layer's last hda to our layer's first hda
                if i != 0 and j == 0:
                    hda.setInput(0, previous_layer_last_hda, 0)
                if j == len(sel_path["hda_ids"]) - 1:
                    previous_layer_last_hda = hda

                # This sets the hda data
                if style is not None:
                    set_hda_parms(hda, db_hda, seed + style[0], obj_name=obj["obj_name"], style=style)
                else:
                    set_hda_parms(hda, db_hda, seed)

                # We need to get the required window, door etc. data from wall
                check_get_styles(obj, hda)

                last_layer_last_hda = hda
        if style is not None:
            attrs = obj["obj_name"].lower() + "Style " + obj["obj_name"].lower() + "Panel"
            attrcopy = hougeo.createNode("attribcopy")
            attrcopy.parm("attribname").set(attrs)
            attrcopy.setInput(0, last_layer_last_hda, 0)
            attrcopy.setInput(1, first_hda, 0)


            pack = hougeo.createNode("pack")
            pack.setInput(0, attrcopy, 0)
            pack.parm("transfer_attributes").set(attrs)
            last_layer_last_hda = pack

        for out in range(len(last_layer_last_hda.outputConnectors())):
            out_fc = hougeo.createNode('filecache')
            out_fc.moveToGoodPosition(move_inputs=False)
            out_fc.parm('filemethod').set(1)
            out_fc.parm('trange').set(0)
            out_fc.parm('file').set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj["obj_name"], project_id=project_id, work_id=work_id, Out=out, id=id) + ".bgeo.sc"))
            out_fc.setInput(0, last_layer_last_hda, out)
            out_fc.parm('execute').pressButton()

        hou.hipFile.save(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj["obj_name"], project_id=project_id, work_id=work_id, Out="0", id=id) + ".hiplc"))

        # TODO maybe add hda name as prefix so there are no overlaps in hda names
        with open(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj["obj_name"], project_id=project_id, work_id=work_id, Out="0", id=id) + ".json"), "w") as f:
            json.dump(obj_parms, f, indent=4)
        return True

    except Exception as e:
        hou.hipFile.save(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + "Errors/" + CACHE_NAME.format(Object=obj["obj_name"], project_id=project_id, work_id=work_id, Out="0", id=id) + ".hiplc"))
        return False


def cast_parm(val, parmtype : str):
    """ Casts the value of first string into type of second string """
    try:
        if parmtype.lower() == "float":
            return float(val)
        elif parmtype.lower() == "int":
            return int(val)
    except Exception as e:
        return e


def place_hda(db_hda, hougeo):
    """ Places the hda in the scene """
    hda_name = db_hda["hda_name"]
    hda_ver = db_hda["hda_version"]

    # TODO seperation of branches
    hda_path = None
    if hda_ver:
        hda_path = f"capoom::dev::{hda_name}::{hda_ver}"
    else:
        hda_path = f"capoom::dev::{hda_name}"

    hda = hougeo.createNode(hda_path)
    return hda

def set_hda_parms(hda, db_hda, seed, obj_name=None, style=None, prediction={}):

    # TODO Check if we really need this. we shouldn't
    if db_hda["hda_name"] == "Null":
        return
    if db_hda["hda_name"] != "StyleCatcher":
        all_parms = db_hda["parm_names"]
        parms_override_mode = db_hda["parm_override_mode"]
        parmmins = db_hda["parm_mins"]
        parmmaxes = db_hda["parm_maxes"]
        parmtypes = db_hda["parm_types"]
        defaults = db_hda["parm_defaults"]




        for parmi, parm in enumerate(all_parms):
            if prediction:
                if parm in prediction.keys():
                    hda.parm(parm).set(prediction[parm])
                    continue
            else:
                seed += 1445
                # This generates a random value for the parm
                if parms_override_mode[parmi] == 1:
                    # Try overriding the minimum value
                    try:
                        if hda.geometry().findGlobalAttrib(parm+"_min"):
                            parmmins[parmi] = hda.geometry().attribValue(parm+"_min")

                    except AttributeError as e:
                        runhda_logger.warn("There are no min attributes in the geometry")

                    # Try overrideng the maximum value

                    try:
                        if hda.geometry().findGlobalAttrib(parm+"_max") is not None:
                            parmmaxes[parmi] = hda.geometry().attribValue(parm+"_max")
                    except AttributeError as e:
                        runhda_logger.warn("There are no max attributes in the geometry")


                    random.seed(seed)
                    overriden_min = cast_parm(parmmins[parmi], parmtypes[parmi])
                    overriden_max = cast_parm(parmmaxes[parmi], parmtypes[parmi])
                    overriden_val_rnd = cast_parm(random.uniform(overriden_min, overriden_max), parmtypes[parmi])
                    try:
                        runhda_logger.info(f"Setting parameter {parm} of {hda.name()} with {overriden_val_rnd}")
                        hda.parm(parm).set(overriden_val_rnd)
                        obj_parms[str(db_hda["hda_name"])][parm] = overriden_val_rnd

                    except AttributeError:
                        runhda_logger.error(f"Attribute couldn't be set: {parm} of {hda.name()}")
                # We need to override to defaults
                else:
                    hda.parm(parm).set(cast_parm(defaults[parmi], parmtypes[parmi]))

                # Check if any of the values got overriden inside the hda
                try:
                    if hda.geometry().findGlobalAttrib(parm+"_actual") is not None:
                        obj_parms[str(db_hda["hda_name"])][parm] = hda.geometry().attribValue(parm+"_actual")
                except AttributeError as e:
                    pass
    else:
        # HARDCODED case for stylecatcher parameters
        hda.parm("object_name").set(obj_name.lower())
        hda.parm("style").set(style[0])
        hda.parm("panel").set(style[1])

        obj_parms[str(db_hda["hda_name"])]["style"] = style[0]
        obj_parms[str(db_hda["hda_name"])]["panel"] = style[0]
        

def check_get_styles(obj, hda):
    if obj in multiple_data_hdas:
        for multiple in multiples:
            # try:
                lowerName = str(multiple["obj_name"].lower())
                # combine two lists into tuple
                temp = set()

                panels = hda.geometry().attribValue(lowerName + "Panels")
                obj_styles = hda.geometry().attribValue(lowerName + "Styles")

                for spi in range(len(obj_styles)):
                    style = obj_styles[spi]
                    panel = panels[spi]
                    temp.add((style, panel))


                all_styles[multiple["obj_name"]] = temp

def create_placer(project_id, work_id, version, parent_structure, object_name, file_count):
    hou.hipFile.clear(suppress_save_prompt=1)
    houobj = hou.node("/obj")
    mergegeo = houobj.createNode("geo")
    
    cur.execute(GET_OBJECT_BY_NAME, (object_name,))
    actual_object = cur.fetchone()
    
    dependent_objects = []
    for data_object in actual_object["needed_data_for_multiple_objs"]:
        cur.execute(GET_OBJECT_BY_ID, (data_object,))
        dependent_objects.append(cur.fetchone())

    filemerge = mergegeo.createNode("filemerge")
    filemerge.moveToGoodPosition(move_inputs=False)
    filemerge.parm("files").set(file_count)

    merge = mergegeo.createNode("merge")

    for id in range(file_count):
        filemerge.parm("filelist" + str(id+1)).set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=object_name, project_id=project_id, work_id=work_id, Out=0, id=id) + ".bgeo.sc"))

    for input_i, dependent_object in enumerate(dependent_objects):
    # We get all the ids of the multiple object that we are trying to place
    # and merge them in file merge


        # We also get the object that we need to place the object on
        wallfc = mergegeo.createNode("filecache")
        wallfc.parm("filemethod").set(1)
        wallfc.parm("loadfromdisk").set(1)
        wallfc.parm("file").set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=dependent_object["obj_name"], project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc"))

        # We create the placer
        placer = mergegeo.createNode("capoom::dev::Placer")
        placer.parm("object_name").set(object_name.lower())
        placer.setInput(0, filemerge)
        placer.setInput(1, wallfc)
        merge.setInput(input_i, placer)

    # We get the output of the placer
    output = mergegeo.createNode("filecache")
    output.parm("filemethod").set(1)
    output.parm("trange").set(0)
    output.parm("file").set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=object_name+"_placed", project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc"))

    output.setInput(0, merge)
    output.parm("execute").pressButton()
    hou.hipFile.save(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=object_name+"_placed", project_id=project_id, work_id=work_id, Out=0, id=0) + ".hiplc"))
    runhda_logger.info(f"Placement done: {object_name}")

def merge_objects_of_structure(project_id, work_id, version, parent_structure="Standalone"):
    hou.hipFile.clear(suppress_save_prompt=1)
    houobj = hou.node("/obj")
    mergegeo = houobj.createNode("geo")

    # Loop over all object folders
    merge_paths = []
    bool_merge_paths = []

    for folder in os.listdir(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure)):
        cur.execute(GET_OBJECT_BY_NAME, (folder,))
        obj_from_db = cur.fetchone()
        if obj_from_db  is not None:
            if obj_from_db["keep"] == True or obj_from_db["keep"] is None:
                if obj_from_db["needed_data_for_multiple_objs"] is not None:
                    merge_paths.append(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj_from_db["obj_name"] + "_placed", project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc")
                # elif obj_from_db["bool_a"] is not None:
                #     bool_merge_paths.append(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj_from_db["obj_name"], project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc")
                else:
                    # We get the number of files that we need to merge
                    merge_paths.append(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj_from_db["obj_name"], project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc")
    
    mergefc = mergegeo.createNode("filemerge")
    mergefc.moveToGoodPosition(move_inputs=False)
    mergefc.parm("files").set(len(merge_paths))

    mergefc_boola = mergegeo.createNode("filemerge")
    mergefc_boola.parm("files").set(len(bool_merge_paths))

    for merge_i, merge_path in enumerate(merge_paths, start=1):
        mergefc.parm("filelist" + str(merge_i)).set(merge_path)
    
    for merge_i, merge_path in enumerate(bool_merge_paths, start=1):
        mergefc_boola.parm("filelist" + str(merge_i)).set(merge_path)

    # cBoolean = mergegeo.createNode("capoom::dev::cBoolean")
    # cBoolean.setInput(0, mergefc_boola)
    # cBoolean.setInput(1, mergefc)

    mergeout = mergegeo.createNode("filecache")
    mergeout.parm("filemethod").set(1)
    mergeout.parm("trange").set(0)
    mergeout.parm("file").set(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"/Merged_{project_id}_{work_id}_{version}.bgeo.sc"))

    merge_all = mergegeo.createNode("merge")
    merge_all.setInput(0, mergefc)

    if len(bool_merge_paths) > 0:
        merge_all.setInput(1, mergefc_boola)
    
    mergeout.setInput(0, merge_all)

    mergeout.parm("execute").pressButton()
    hou.hipFile.save(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"/Merged_{project_id}_{work_id}_{version}.hiplc"))
def assign_materials(object_name, geo, node):
    #------------------------------------#
    import hou
    import random
    obj = hou.node("/obj")
    geo = hou.node(f"{obj.path()}/geo1")
    node = hou.node(f"{geo.path()}/Wall_Placement1")
    geom = node.geometry()
    object_name = "Wall"
    seed = 42
    #------------------------------------#
    
    materials = {}
    for prim in geom.prims():
        attr_material = prim.attribValue("material")
        prim_num = prim.number()
        if attr_material not in materials.keys():
            random.seed(seed)
            materials[attr_material] = (random.choice(attr_material),[])
        materials[attr_material][1].append(str(prim_num))

    for i,material in enumerate(materials.keys()):
        previus_node = node
        if i > 0:
            previus_node = hou.node(f"{geo.path()}/attribcreate_{str(i-1)}")

        attribcreate = geo.createNode(f"attribcreate", f"attribcreate_{str(i)}")
        attribcreate.setInput(0, previus_node)
        attribcreate.moveToGoodPosition()
        prim_nums = ", ".join(materials[material][1]) 
        attribcreate.parm("group").set(f"{prim_nums}")
        attribcreate.parm("name1").set("path")
        attribcreate.parm("type1").set(3)
        attribcreate.parm("string1").set(f"/{object_name}/{materials[material][0]}/")




def init_creation():
    global conn, cur, multiples, multiple_data_hdas, all_styles

    credentials = get_credentials()
    dbname = credentials["db_name"]
    user = credentials["db_user"]
    password = credentials["db_password"]
    host = credentials["db_host"]
    port = credentials["db_port"]


    conn = psycopg2.connect(f"dbname={dbname} user={user} password={password} host={host}, port={port}")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    

    cur.execute(GET_MULTIPLE_OBJECTS)
    # This is a string array of names of those objects
    multiples = cur.fetchall()
    
    # This is a string array of hda's that store the needed data
    multiple_data_hdas = []

    # runhda_logger.info("Multiples", multiples)
    # Loop over all objects that need multiple instances
    for multiple in multiples:
        # The object ids that data comes from
        mult_object_ids = multiple["needed_data_for_multiple_objs"]
        for mult_object_id in mult_object_ids:
            # runhda_logger.info("Mult object id", mult_object_id)
            cur.execute(GET_OBJECT_BY_ID, (mult_object_id,))
            mult_object = cur.fetchone()
            if mult_object is not None:
                multiple_data_hdas.append(mult_object)

    # runhda_logger.info("Data hdas", multiple_data_hdas)

    # This dictionary contains the data of the objects that have multiple choices Tuple(Style, Panel)
    all_styles = dict()

    # create_structure("House", 112358, 30, 2)
    # create_object(1, 60, 1)
import psycopg2
import psycopg2.extras
import random
import sys,os
import json
import collections
import traceback
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
GET_OBJECTS_BY_IDS = """SELECT * FROM "Objects" WHERE obj_id IN %s"""
GET_OBJECT_BY_NAME = """SELECT * FROM "Objects" WHERE obj_name = %s"""
GET_COMPS_BY_ID = """SELECT * FROM "Components" WHERE component_id = %s"""
GET_PATHS_BY_ID = """SELECT * FROM "Paths" WHERE path_id = %s"""
GET_HDA_BY_ID = """SELECT * FROM "Hdas" WHERE hda_id = %s"""
GET_MULTIPLE_OBJECTS ="""SELECT * FROM "Objects" WHERE needed_data_for_multiple_objs NOTNULL"""
GET_HDA_PARMS = """ SELECT * FROM "Parameters" WHERE hda_id = %s"""

# Passing the logger from slave to here
runhda_logger = None
def init_logger(logger):
    global runhda_logger
    runhda_logger = logger
    runhda_logger.info("Runhda logger initialized")

def create_structure(structname, project_id, work_id, version, parm_template={}, export=[]):
    # Format XXXX
    version = str(version).zfill(4)

    # TODO remove count, instead use workid
    cur.execute(GET_STRUCT_BY_NAME, (structname,))
    structure = cur.fetchone()

    runhda_logger.info(f'Creating structure {structure["structure_name"]}')

    object_ids = structure["obj_ids"]
    obj_creation_results = []

    # We store the objects we skipped so we skip the children of them as well
    global skipped_object_ids
    skipped_object_ids = []

    for obj_id in object_ids:
        cur.execute(GET_OBJECT_BY_ID, (obj_id,))
        obj = cur.fetchone()

        obj_can_skip = obj["obj_can_skip"]
        obj_skip_chance = obj["obj_skip_chance"]
        if obj_can_skip:
            if random.random() <= obj_skip_chance:
                runhda_logger.info(f'Skipping object {obj["obj_name"]}')
                skipped_object_ids.append(obj_id)
                continue

        if obj in multiples:
            # We need to get rid of duplicates
            obj_styles = all_styles[obj["obj_name"]]
            runhda_logger.info(f'Creating object {obj["obj_name"]} with {len(obj_styles)} styles')
            for style_counter, obj_style in enumerate(obj_styles):
                runhda_logger.info(f'Creating object {obj["obj_name"]} with style {obj_style}')
                result = create_object(obj_id, project_id, work_id, version, parent_structure=structname, style=obj_style, id=style_counter, parm_template=parm_template, export=export)
                obj_creation_results.append(result)

            create_placer(project_id, work_id, version, structname, obj["obj_name"], len(obj_styles))
        else:
            result = create_object(obj_id, project_id, work_id, version, parent_structure=structname, parm_template=parm_template, export=export)
            obj_creation_results.append(result)

    merge_objects_of_structure(project_id, work_id, version, parent_structure=structname, export=export)

    if all(obj_creation_results):
        runhda_logger.info("Structure created successfully")
        return True
    else:
        runhda_logger.info("Structure created but it has failed objects")
        return False
    # do stuff with cache_name


# TODO handle the save path errors that raises when we dont have a parent structure

def create_object(obj_id, project_id, work_id, version, parent_structure="Standalone", style=None, id=0, prediction_parms={}, parm_template={}, export=[]):
    try:
        cur.execute(GET_OBJECT_BY_ID, (obj_id,))
        obj = cur.fetchone()
        runhda_logger.info(f'Creating object {obj["obj_name"]}')


        # we can rename this after
        dependent_objs_ids = obj["dependent_obj_ids"]
        dependent_objs_outs = obj["dependent_obj_outs"]
        contradictive_obj_ids = obj["contradictive_obj_ids"]
        # We need to check if we have skipped objects in our dependencies
        # if so, we skip this object as well
        if dependent_objs_ids:
            for dep_obj_id in dependent_objs_ids:
                if dep_obj_id in skipped_object_ids:
                    runhda_logger.info(f'Skipping object {obj["obj_name"]} due to skipped dependency')
                    skipped_object_ids.append(obj_id)
                    return True

        if contradictive_obj_ids:
            for contradictive_obj_id in contradictive_obj_ids:
                if contradictive_obj_id not in skipped_object_ids:
                    runhda_logger.info(f'Skipping object {obj["obj_name"]} due to contradictive dependency')
                    skipped_object_ids.append(obj_id)
                    return True

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
        for layer_index, layer_id in enumerate(layer_ids):
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


            for hda_index, hda_id in enumerate(sel_path["hda_ids"]):
                cur.execute(GET_HDA_BY_ID, (hda_id,))
                db_hda = cur.fetchone()

                seed = project_id + work_id + obj_id + 5987

                hda = None

                # This is a special hardcoded case,
                # we sometimes use nulls to get caches of outputs of some object as a seperate object by itself
                # (i.e WallFromPorch)
                # if db_hda["hda_name"] == "Null":
                #     hda=hougeo.createNode("null")
                # else:
                hda = place_hda(db_hda, hougeo, parm_template)

                if db_hda["hda_name"] == "TerrainCreator":
                    try:
                        area_blast=hougeo.createNode("blast")
                        area_blast.parm("group").set(f"@areaId={work_id}")
                        area_blast.parm("negate").set(1)
                        area_blast.setInput(0, hda)
                        hda=area_blast
                    except Exception as e:
                        # This is thrown when we request a terrain work that has more house than the area
                        # We need to handle this better
                        runhda_logger.error(f"Error while creating terrain {e}\n This probably means that the area has more houses than it can have")
                        return False


                if layer_index == hda_index == 0:
                    first_hda = hda


                    # FIXME this is a big hardcoded situation, we need to find a better way to do this
                    # The problem with this is, this lines of codes makes the dependency system obsolete
                    # We need to find a way to make this work with the dependency system. for example,
                    # if we wanted to make the multiple object have another input dependency we simply cant
                    if style is not None:

                        # We need to merge our data hdas
                        data_obj_ids = obj["needed_data_for_multiple_objs"]

                        cur.execute(GET_OBJECTS_BY_IDS, (tuple(data_obj_ids),))
                        data_objs = cur.fetchall()

                        for data_obj in data_objs:
                            if data_obj["obj_id"] in skipped_object_ids:
                                data_objs.remove(data_obj)

                        data_obj_cache_paths = []
                        for data_obj in data_objs:
                            data_obj_name = data_obj["obj_name"]
                            # Get the path of the data object cache
                            data_obj_cache_path = str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=data_obj_name, project_id=project_id, work_id=work_id, Out="0", id=0) + ".bgeo.sc")
                            data_obj_cache_paths.append(data_obj_cache_path)

                        first_hda_in_fc = hougeo.createNode("filemerge")
                        first_hda_in_fc.parm("files").set(len(data_obj_cache_paths))

                        for data_obj_i, data_obj_cache_path in enumerate(data_obj_cache_paths, start=1):
                            first_hda_in_fc.parm("filelist" + str(data_obj_i)).set(data_obj_cache_path)

                        first_hda.setInput(0, first_hda_in_fc)

                    # Here we place the filecaches needed for the dependencies
                    else:
                        if dependent_objs_ids and dependent_objs_outs:
                            # We have dependencies
                            file_caches = []
                            for dep_i, dep_id in enumerate(dependent_objs_ids):
                                cur.execute(GET_OBJECT_BY_ID, (dep_id,))
                                dep_obj = cur.fetchone()

                                # Place the filecache
                                first_hda_in_fc = hougeo.createNode("filecache")

                                if dep_id == -1:
                                    # TODO make the house part more generic
                                    filepath = str(MERGE_PATH.format(project_id=project_id, version=version, structure="House") + f"Bgeo/Bgeo_{project_id}_{work_id}_{version}.bgeo.sc")
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
                if layer_index != 0 and hda_index == 0:
                    hda.setInput(0, previous_layer_last_hda, 0)

                if hda_index == len(sel_path["hda_ids"]) - 1:
                    previous_layer_last_hda = hda

                # This sets the hda data
                if style is not None:
                    set_hda_parms(hda, db_hda, seed + style[0], obj_name=obj["obj_name"], style=style, parm_template=parm_template)
                else:
                    set_hda_parms(hda, db_hda, seed, parm_template=parm_template)


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
            mat_path_node = None
            if out == 0:
                try:
                    mat_path_node = assign_materials(obj["obj_name"], hougeo, hda, seed)
                except Exception as e:
                    mat_path_node = None
                    runhda_logger.warn(e)


            out_fc = hougeo.createNode('filecache')
            out_fc.moveToGoodPosition(move_inputs=False)
            out_fc.parm('filemethod').set(1)
            out_fc.parm('trange').set(0)
            out_fc.parm('file').set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj["obj_name"], project_id=project_id, work_id=work_id, Out=out, id=id) + ".bgeo.sc"))

            if (mat_path_node != last_layer_last_hda and out == 0) or mat_path_node is not None:
                # runhda_logger.opus(f"Setting the input of the filecache to the material path node {mat_path_node}")
                out_fc.setInput(0, mat_path_node, out)
            else:
                # runhda_logger.opus(f"Setting the input of the filecache to the last layer last hda {last_layer_last_hda}")
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
        elif parmtype.lower() == "string":
            return val
        else:
            raise Exception(f"{parmtype} is not a supported type")
    except Exception as e:
        runhda_logger.error(f"Could not cast {val} to {parmtype}")
        return traceback.format_exc()

def place_hda(db_hda, hougeo, parm_template={}):
    """ Places the hda in the scene """
    hda_name = db_hda["hda_name"]
    hda_ver = None
    hda_id = db_hda["hda_id"]
    hda_branch = db_hda["hda_branch"]

    if parm_template != {}:
        if f"Hdas_{hda_id}" in parm_template:
            hda_ver = parm_template[f"Hdas_{hda_id}.version"]

    if hda_ver is None:
        runhda_logger.warn("Version not found in template! Using the latest version of the hda")
        selected_parm = get_hdaparms_highest_version(db_hda["hda_id"])
        hda_ver = selected_parm["hda_version"]
        runhda_logger.info(f"Selected version of {hda_name} is {hda_ver}")
    
    hda_path = get_hda_path(hda_name, hda_ver, hda_branch)
    
    try:
        hda = hougeo.createNode(hda_path)
    except Exception as e:
        runhda_logger.error(f"Could not place {hda_path}\nThis might be a template problem! Check the template for {hda_name}\nError:{e}")
        return traceback.format_exc()
    return hda

def get_hda_path(hda_name, hda_ver, hda_branch):
    path = ""
    if hda_branch:
        path += f"{hda_branch}::"
    if hda_name is not None:
        path += f"{hda_name}"
    else:
        raise ValueError("Hda name is not defined")
    
    if hda_ver is not None:
        path += f"::{hda_ver}"
    
    return path

def set_hda_parms(hda, db_hda, seed, obj_name=None, style=None, prediction={}, parm_template={}):
    hda_name = db_hda["hda_name"]

    # TODO Check if we really need this. we shouldn't
    if hda_name == "null":
        return
    if hda_name != "StyleCatcher":
        parm_names, parm_mins, parm_maxes, parm_defaults, parm_override_modes, parm_types = [], [], [], [], [], []

        if parm_template:
            parm_names, parm_mins, parm_maxes, parm_defaults, parm_override_modes, parm_types = get_random_rule_hda(parm_template, db_hda["hda_id"])
        else:
            runhda_logger.info(f"No parm template found for {hda_name}! Using the latest version of the hda")


            selected_parm = get_hdaparms_highest_version(db_hda["hda_id"])

            if selected_parm:
                parm_names = selected_parm["parm_name"]
                parm_mins = selected_parm["parm_min"]
                parm_maxes = selected_parm["parm_max"]
                parm_defaults = selected_parm["parm_default"]
                parm_override_modes = selected_parm["parm_override"]
                parm_types = selected_parm["parm_type"]



        for parmi, parm in enumerate(parm_names):
            if prediction:
                if parm in prediction.keys():
                    hda.parm(parm).set(prediction[parm])
                    continue
            else:
                seed += 1445
                # Look at the detail attributes and see if we need to override the parm
                if parm_override_modes[parmi] == 1:
                    try:
                        if hda.geometry().findGlobalAttrib(parm+"_min"):
                            parm_mins[parmi] = hda.geometry().attribValue(parm+"_min")

                    except AttributeError as e:
                        runhda_logger.warn("There are no min attributes in the geometry")

                    try:
                        if hda.geometry().findGlobalAttrib("opus_"+parm+"_max") is not None:
                            parm_maxes[parmi] = hda.geometry().attribValue("opus_"+parm+"_max")
                    except AttributeError as e:
                        runhda_logger.warn("There are no max attributes in the geometry")

                    random.seed(seed)

                    overriden_min = cast_parm(parm_mins[parmi], parm_types[parmi])
                    overriden_max = cast_parm(parm_maxes[parmi], parm_types[parmi])
                    overriden_val_rnd = cast_parm(random.uniform(overriden_min, overriden_max), parm_types[parmi])
                    try:
                        runhda_logger.info(f"Setting parameter {parm} of {hda.name()} with {overriden_val_rnd}")
                        hda.parm(parm).set(overriden_val_rnd)
                        obj_parms[str(db_hda["hda_name"])][parm] = overriden_val_rnd

                    except AttributeError:
                        runhda_logger.error(f"Attribute couldn't be set: {parm} of {hda.name()}")
                # We need to override to defaults
                else:
                    hda.parm(parm).set(cast_parm(parm_defaults[parmi], parm_types[parmi]))

                # Check if any of the values got overriden inside the hda
                try:
                    if hda.geometry().findGlobalAttrib("opus_"+parm+"_actual") is not None:
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
                try:
                    panels = hda.geometry().attribValue(lowerName + "Panels")
                    obj_styles = hda.geometry().attribValue(lowerName + "Styles")
                except Exception as e:
                    runhda_logger.info(f"Couldn't find {lowerName}Panels or {lowerName} Styles in {hda.name()}")
                    return

                for spi in range(len(obj_styles)):
                    style = obj_styles[spi]
                    panel = panels[spi]
                    temp.add((style, panel))

                runhda_logger.info(f"Found {len(temp)} styles for {multiple['obj_name']}")

                if multiple["obj_name"] not in all_styles.keys():
                    all_styles[multiple["obj_name"]] = temp
                else:
                    all_styles[multiple["obj_name"]].update(temp)

                runhda_logger.info(f"Styles for {multiple['obj_name']}: {all_styles[multiple['obj_name']]}")

def create_placer(project_id, work_id, version, parent_structure, object_name, file_count):
    hou.hipFile.clear(suppress_save_prompt=1)
    houobj = hou.node("/obj")
    mergegeo = houobj.createNode("geo")

    cur.execute(GET_OBJECT_BY_NAME, (object_name,))
    actual_object = cur.fetchone()

    dependent_objects = []
    for data_object in actual_object["needed_data_for_multiple_objs"]:
        cur.execute(GET_OBJECT_BY_ID, (data_object,))
        dep_obj = cur.fetchone()
        if dep_obj["obj_id"] not in skipped_object_ids:
            dependent_objects.append(dep_obj)

    filemerge = mergegeo.createNode("filemerge")
    filemerge.moveToGoodPosition(move_inputs=False)
    filemerge.parm("files").set(file_count)

    merge = mergegeo.createNode("merge")

    for id in range(file_count):
        filemerge.parm("filelist" + str(id+1)).set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=object_name, project_id=project_id, work_id=work_id, Out=0, id=id) + ".bgeo.sc"))

    for input_i, dependent_object in enumerate(dependent_objects):

        placed_on = mergegeo.createNode("filecache")
        placed_on.parm("filemethod").set(1)
        placed_on.parm("loadfromdisk").set(1)
        placed_on.parm("file").set(str(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=dependent_object["obj_name"], project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc"))

        # We create the placer
        placer = mergegeo.createNode("capoom::dev::Placer")
        placer.parm("object_name").set(object_name.lower())
        placer.setInput(0, filemerge)
        placer.setInput(1, placed_on)
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

def merge_objects_of_structure(project_id, work_id, version, parent_structure="Standalone", export=[]):
    hou.hipFile.clear(suppress_save_prompt=1)
    houobj = hou.node("/obj")
    mergegeo = houobj.createNode("geo")

    # Loop over all object folders
    merge_paths = []

    for folder in os.listdir(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure)):
        cur.execute(GET_OBJECT_BY_NAME, (folder,))
        obj_from_db = cur.fetchone()

        if obj_from_db is not None:
            if obj_from_db["obj_id"] in skipped_object_ids:
                continue

            if obj_from_db["keep"] == True or obj_from_db["keep"] is None:
                if obj_from_db["needed_data_for_multiple_objs"] is not None:
                    merge_paths.append(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj_from_db["obj_name"] + "_placed", project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc")
                else:
                    # We get the number of files that we need to merge
                    merge_paths.append(SAVE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + CACHE_NAME.format(Object=obj_from_db["obj_name"], project_id=project_id, work_id=work_id, Out=0, id=0) + ".bgeo.sc")

    mergefc = mergegeo.createNode("filemerge")
    mergefc.moveToGoodPosition(move_inputs=False)
    mergefc.parm("files").set(len(merge_paths))


    for merge_i, merge_path in enumerate(merge_paths, start=1):
        mergefc.parm("filelist" + str(merge_i)).set(merge_path)

    merge_out = mergegeo.createNode("null")
    merge_out.moveToGoodPosition(move_inputs=False)
    merge_out.setInput(0, mergefc)

    # -- EXPORT
    if "bgeo.sc" in export:
        runhda_logger.opus("Exporting bgeo")
        try:
            export_bgeo(mergegeo, merge_out, project_id, version, parent_structure, work_id)
        except Exception as e:
            runhda_logger.error(f"Error while exporting bgeo: {e}")
    
    if "pointcloud" in export:
        runhda_logger.opus("Exporting pointcloud")
        try:
            export_pc_as_xyz(mergegeo, merge_out, project_id, version, parent_structure, work_id)
        except Exception as e:
            runhda_logger.error(f"Error while exporting pointcloud: {e}")
    if "wireframe" in export:
        runhda_logger.opus("Exporting wireframe")
        try:
            export_wireframe(mergegeo, merge_out, project_id, version, parent_structure, work_id)
        except Exception as e:
            runhda_logger.error(f"Error while exporting wireframe: {e}")

    if "hip" in export:
        runhda_logger.opus("Exporting hip")
        try:
            export_hip(project_id, version, parent_structure, work_id)
        except Exception as e:
            runhda_logger.error(f"Error while exporting hip: {e}")
        # hou.hipFile.save(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"/Merged_{project_id}_{work_id}_{version}.hiplc"))

def assign_materials(object_name, geo, node, seed):
    """Assigns materials names to path of the objects based on the material attribute of the primitives \n
    object_name: Name of the object to assign materials \n
    geo: geo node of the object \n
    node: node of the object \n
    Returns: Last node \n"""
    #------------------------------------#
    geom = node.geometry()

    if geom is None:
        runhda_logger.warn(f"Object {object_name} has no geometry")
        return node

    materials = {}
    attribcreate = None

    for prim in geom.prims():

        # Check if prim has an attribute called material
        try:
            attr_material = prim.attribValue("opus_material")
        except hou.OperationFailed:
            runhda_logger.warn(f"Object {object_name} has no material attribute")
            return node

        prim_num = prim.number()
        if attr_material not in materials.keys():
            random.seed(seed)
            sel_mat = random.choice(attr_material)
            materials[attr_material] = [sel_mat, []]
        materials[attr_material][1].append(str(prim_num))

    for i,material in enumerate(materials.keys()):
        previous_node = node
        if i > 0:
            previous_node = hou.node(f"{geo.path()}/attribcreate_{str(i-1)}")

        attribcreate = geo.createNode(f"attribcreate", f"attribcreate_{str(i)}")
        attribcreate.setInput(0, previous_node)
        attribcreate.moveToGoodPosition()
        prim_nums = ", ".join(materials[material][1])
        attribcreate.parm("group").set(f"{prim_nums}")
        attribcreate.parm("name1").set("path")
        attribcreate.parm("class1").set(1)
        attribcreate.parm("type1").set(3)
        attribcreate.parm("string1").set(f"/{object_name}/{materials[material][0]}/")
    return attribcreate

def get_hdaparms_highest_version(hda_id):
    cur.execute(GET_HDA_PARMS, (hda_id,))
    db_parms = cur.fetchall()
    highest_version = max([parm["hda_version"] for parm in db_parms])
    selected_parm = None
    for parm in db_parms:
        if parm["hda_version"] == highest_version:
            selected_parm = parm

    return selected_parm

def pick_random_rule(hda_rules):
    # First indices are the rules themselves, second indices are the weight of that rule
    rules = [x[0] for x in hda_rules]
    weights = [x[1] for x in hda_rules]

    random_rule = random.choices(rules, weights=weights, k=1)[0]
    return random_rule

def get_random_rule_hda(all_rules, hda_name):

    parms = []
    for rule in all_rules:
        if rule == f"Hdas_{hda_name}":
            parms = all_rules[rule]
            break
    parm_names, parm_mins, parm_maxes, parm_defaults, parm_override_modes, parm_types = [], [], [], [], [], []

    for parm in parms:
        rule = pick_random_rule(parms[parm])
        parm_names.append(parm)
        parm_mins.append(rule[0])
        parm_maxes.append(rule[1])
        parm_defaults.append(rule[2])
        parm_override_modes.append(rule[3])
        parm_types.append(rule[4])

    return parm_names, parm_mins, parm_maxes, parm_defaults, parm_override_modes, parm_types

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++ EXPORT FUNCTIONS +++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

def export_pc_as_xyz(hougeo, node, project_id, version, parent_structure, work_id):
    # TODO make the export a dictionary rather than a list, so that we can add more settings to the specific export type, such as point count, export format etc
    """ Exports the pointcloud of the given node using houdini's scatter node\n
    `hougeo` is the geo obj of the houdini scene\n
    `node` is the node to export the pointcloud of\n
    `project_id` is the id of the project\n
    `version` is the version of the project\n
    `parent_structure` is the structure of the project\n
    `work_id` is the id of the work
    """
    if node is None:
        return

    normalize_geo_size = hougeo.createNode("capoom::dev::normalize_geo_size")
    normalize_geo_size.setInput(0, node, 0)
    
    pc = hougeo.createNode("scatter")
    pc.parm("relaxpoints").set(0)
    pc.parm("npts").set(100000)
    pc.setInput(0, normalize_geo_size, 0)


    pc_points = pc.geometry().points()
    
    ptpos = []
    for pt in pc_points:
        ptpos.append(pt.attribValue("P"))

    # Check if the directory exists, if not create it
    if not os.path.exists(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Point_Cloud/"):
        os.makedirs(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Point_Cloud/")
    
    # check if the file exists, if not, create it
    with open(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Point_Cloud/PC_{project_id}_{work_id}_{version}.xyz"), "w") as f:
        for pt in ptpos:
            f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")

def export_bgeo(hougeo, node, project_id, version, parent_structure, work_id):
    """ Exports the bgeo of the given node\n
        `hougeo` is the geo obj of the houdini scene\n
        `node` is the node to export the bgeo of\n
        `project_id` is the id of the project\n
        `version` is the version of the project\n
        `parent_structure` is the structure of the project\n
        `work_id` is the id of the work\n"""
    
    bgeoout = hougeo.createNode("filecache")
    bgeoout.parm("filemethod").set(1)
    bgeoout.parm("trange").set(0)
    bgeoout.parm("file").set(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Bgeo/Bgeo_{project_id}_{work_id}_{version}.bgeo.sc"))
    bgeoout.setInput(0, node)

    bgeoout.parm("execute").pressButton()

def export_wireframe(hougeo, node, project_id, version, parent_structure, work_id):
    """ Exports the wireframe of the given node\n
        `hougeo` is the geo obj of the houdini scene\n
        `node` is the node to export the wireframe of\n
        `project_id` is the id of the project\n
        `version` is the version of the project\n
        `parent_structure` is the structure of the project\n
        `work_id` is the id of the work
        """

    wf = hougeo.createNode("capoom::dev::house_wireframe")
    wf.setInput(0, node)
    
    mergeoutobj = hougeo.createNode("filecache")
    mergeoutobj.parm("filemethod").set(1)
    mergeoutobj.parm("trange").set(0)
    mergeoutobj.parm("file").set(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Wireframe/Wireframe_{project_id}_{work_id}_{version}.obj"))

    mergeoutobj.setInput(0, wf)
    mergeoutobj.parm("execute").pressButton()

def export_hip(project_id, version, parent_structure, work_id):
    # Check if the directory exists, if not create it
    if not os.path.exists(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Hip/"):
        os.makedirs(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Hip/")

    hou.hipFile.save(str(MERGE_PATH.format(project_id=project_id, version=version, structure=parent_structure) + f"Hip/Hip_{project_id}_{work_id}_{version}.hiplc"))

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

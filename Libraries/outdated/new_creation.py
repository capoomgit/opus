


# TODO: Nullcheck for all functions

# def create_structure(struct_name):
#     struct = cur.execute(GET_STRUCT_BY_NAME, (struct_name,))
#     objs = struct["objs"]

#     for obj in objs:
#         create_obj(obj)
    
# # Creates the given obj
# def create_obj(obj_id):
#     obj = cur.execute(GET_OBJ_BY_ID, (obj_id,))
#     layers = obj["layers"]

    
#     for i, layer in enumerate(layers):
#         create_lyr(layer)


# def create_lyr(layer_id):
#     lyr = cur.execute(GET_LYR_BY_ID, (layer_id,))
#     paths = lyr["paths"]
    
#     for path in paths:
#         create_path(prev_layer, path)

# def create_path(layer, path_id):
#     path = cur.execute(GET_PATH_BY_ID, (path_id,))
#     hdas = path["hdas"]
    
#     for hda in hdas:
#         cache_hda(layer, hda)

# def cache_hda(layer, hda_id):
#     hda = cur.execute(GET_HDA_BY_ID, (hda_id,))
    
#     # These are the additional hda cachces that this particular hda needs, 
#     # if these are null we just need to connect to the previous layers chosen paths last node
#     previous_nodes = hda["prev_nodes"]
#     previous_outs = hda["prev_outs"]

#     if not previous_nodes and not previous_outs:
#         # We just have to connect to the previous layers chosen paths last node
        
#         pass
#     else:
#         # We have to cache the previous nodes and connect to them
#         pass


# def window_layer():
#     pass
# if __name__ == "__main__":
#     # connection info is wrong
#     conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
#     # create_obj("Floor")
#     # create_obj("Wall")
#     # create_obj("Porch")
#     # create_obj("Roof")


import psycopg2
import psycopg2.extras
import random

GET_STRUCT_BY_NAME = """SELECT * FROM public.Structures WHERE name = %s"""
GET_OBJ_BY_ID = """SELECT * FROM public.Objects WHERE id = %s"""
GET_LYR_BY_ID = """SELECT * FROM public.Layers WHERE id = %s"""
GET_PATH_BY_ID = """SELECT * FROM public.Paths WHERE id = %s"""
GET_HDA_BY_ID = """SELECT * FROM public.Hda WHERE id = %s"""

GET_PREV_PATH_BY_HDA_ID = """SELECT * FROM public."Paths" WHERE "objects" @> ARRAY[%s]::integer[] """
GET_PREV_LAYER_BY_PATH_ID = """SELECT * FROM public."Layers" WHERE "objects" @> ARRAY[%s]::integer[] """
GET_PREV_OBJ_BY_LAYER_ID = """SELECT * FROM public."Objects" WHERE "objects" @> ARRAY[%s]::integer[] """


SAVE_DIR = "P:/pipeline/standalone_dev/saved/"

def create_structure(structname, project_id, work_id):
    struct = cur.execute(GET_STRUCT_BY_NAME, (structname,))
    objs = struct["objects"]

    # This is ordered by creation priority
    for obj in objs:
        create_obj(obj, project_id, work_id, structname)


def create_obj(obj_id, project_id, work_id, structname):
    obj = cur.execute(GET_OBJ_BY_ID, (obj_id,))
    layers = obj["layers"]

    # Window
    # if obj["name"] == "Window":
    
    for i, layer in enumerate(layers):
        paths = layer["paths"]
        
        random.seed(project_id + work_id + i)
        sel_path_id = random.choice(paths)

        sel_path = cur.execute(GET_PATH_BY_ID, (sel_path_id,))
        hda_ids = sel_path["hdas"]
        
        hdas = []
        for hda_id in hda_ids:
            hdas.append(cur.execute(GET_HDA_BY_ID, (hda_ids,)))
        
        for hda in hdas:
            previous_nodes = hda["prev_nodes"]
            previous_outs = hda["prev_outs"]

            if not previous_nodes and not previous_outs:
                # This is manifold
                # TODO execute and cache hda
                continue
            
            if len(previous_nodes) > 1:
                for previous_node in previous_nodes[1:]:
                    # TODO load from cache the previous 
                    pass
            
            if previous_nodes[0] is not None:
                # TODO load from cache the previous node

                prev_path_id = cur.execute(GET_PREV_PATH_BY_HDA_ID, (previous_nodes[0],))["id"]
                prev_layer_id = cur.execute(GET_PREV_LAYER_BY_PATH_ID, (prev_path_id,))["id"]
                prev_obj_name = cur.execute(GET_PREV_OBJ_BY_LAYER_ID, (prev_layer_id,))["name"]

                hda_dir = f"{SAVE_DIR}/{structname}/{prev_obj_name}/Out_{previous_outs[0]}"
            elif previous_nodes[0] is None:
                pass
                # Done with inputs except 0,
                # TODO get the last node of previous layer and set it to the first input of this hda
                
            # else:
            #     raise Exception("Something really went wrong")
                # We should never be here
if __name__ == "__main__":
    # connection info is wrong
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    

    create_structure("House", 1, 1)
    # create_object("Floor")




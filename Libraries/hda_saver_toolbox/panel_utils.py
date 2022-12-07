from msilib import init_database
import hou
from hda_register import hda_register
from database import Database, CursorFromConnectionFromPool
import sys

GET_LAYER_BY_NAME = """SELECT * FROM "Components" WHERE component_name = %s"""
GET_NODE_BY_NAME = """SELECT * FROM "Hdas" WHERE hda_name = %s"""
UPDATE_NODE_BY_NAME = """UPDATE "Hdas" SET parm_names = %s, parm_defaults = %s, parm_mins = %s, parm_maxes = %s, parm_types = %s, hda_version = %s WHERE hda_name = %s RETURNING hda_id"""
SAVE_LAYER = """INSERT INTO "Components" (component_name, path_ids, can_skip, skip_chance) VALUES (%s, %s, %s, %s)"""
SAVE_PATH = """INSERT INTO "Paths" (hda_ids) VALUES (%s) RETURNING path_id"""
DELETE_HDA_BY_NAME = """DELETE FROM "Hdas" WHERE hda_name = %s RETURNING hda_id"""
UPDATE_PATH = """UPDATE "Paths" SET hda_ids = %s WHERE id = %s"""

def save_layer():
    """Export the selected node parms to a database"""
    selected_nodes = hou.selectedNodes()
    selected_nodes = [x for x in selected_nodes]

    # Sort the nodes by hierarchy

    layer_start, layer_end = None, None
    layer_name_start, layer_name_end = None, None

    for node in selected_nodes:
        if node.name().startswith("LayerStart"):
            layer_start = node
            layer_name_start = node.name().replace("LayerStart", "")
        if node.name().startswith("LayerEnd"):
            layer_end = node
            layer_name_end = node.name().replace("LayerEnd", "")

    if layer_name_start != layer_name_end:
        hou.ui.displayMessage("The selected nodes are not in the same layer")
        return
    else:
        layer_name = layer_name_start

    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(GET_LAYER_BY_NAME, (layer_name,))
        layer = cursor.fetchone()
        if layer is not None:
            hou.ui.displayMessage(f"The layer with name {layer_name} already exists")
            return
        else:
            print("Layer does not exist, we are all good")

    if layer_start and layer_end:
        print("Start and End found for layer", layer_name)

    switch = None
    if layer_end.inputConnections()[0].inputNode().name().replace(str(layer_end.inputConnections()[0].inputNode().digitsInName()), "") == "switch":
        print("switch found")
        switch = layer_end.inputConnections()[0].inputNode()
    else:
        hou.ui.displayMessage("Please add a switch before the layer end")


    # sys.setrecursionlimit(10000)


    # recursion to find all paths that lead to the root node
    def find_path(cur_node, path=[]):

        # if the output is connected to the layer start node
        if cur_node.inputConnections()[0].inputNode().name().startswith("LayerStart"):
            return path
        else:
            parent = cur_node.inputConnections()[0].inputNode()
            return find_path(parent, path + [parent])

    paths = []
    for inp in switch.inputConnections():
        path_end = inp.inputNode()
        print(path_end.name())

        path = find_path(path_end, path=[path_end])
        # Check here if the all the nodes belong to the capoom company
        if path:
            path.reverse()
            paths.append(path)

    print(paths)

    path_db_ids = []
    for path in paths:
        ids = save_nodes(nodes_to_save=path)
        print(ids)
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(SAVE_PATH, (ids,))
            path_db_ids.append(cursor.fetchone()[0])

    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(SAVE_LAYER, (layer_name, path_db_ids, False, 0.0))


def save_nodes(nodes_to_save=None):
    if not nodes_to_save:
        nodes_to_save = list(hou.selectedNodes())
        print(nodes_to_save)

    corresponding_ids = []
    for selected_node in nodes_to_save:
        exist = False
        company = hou.hda.componentsFromFullNodeTypeName(selected_node.type().name())
        version = company[3]
        node_name = company[2]
        company = company[1].split(":")


        # Get the hda version

        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(GET_NODE_BY_NAME, (node_name,))
            node = cursor.fetchone()
            if node is not None:
                print("Node already exists")
                exist = True
            else:
                print("Node does not exist, we are all good")
        all_parms = []
        parms_default = []
        parms_min = []
        parms_max = []
        parms_type = []
        parms_override = []
        # get all the parms of the selected node

        for parm in selected_node.parms():
            try:
                if parm.parmTemplate().type() != hou.parmTemplateType.FolderSet and parm.parmTemplate().type() != hou.parmTemplateType.Toggle and parm.parmTemplate().type() != hou.parmTemplateType.Label:
                    all_parms.append(parm.name())
                    parms_default.append(parm.eval())
                    parms_min.append(parm.parmTemplate().minValue())
                    parms_max.append(parm.parmTemplate().maxValue())
                    #get the type of the parm as string and add it to the list
                    parms_type.append(str(parm.parmTemplate().type()).split(".")[-1])
                    parms_override.append(1)
            except Exception as e:
                print(e)
                print("Error while saving", node_name)

        # Save the node
        if not exist:
            hda = hda_register(node_name, all_parms, parms_default, parms_min, parms_max, parms_type, parms_override, version)
            id = hda.save_to_db()
            corresponding_ids.append(id)
            print("Saved to database", node_name)
        else:
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute(UPDATE_NODE_BY_NAME, (all_parms, parms_default, parms_min, parms_max, parms_type, version, node_name))
                corresponding_ids.append(node[0])
                print("Updated database", node_name)
    return corresponding_ids

def delete_hdas(nodes=None):

    if not nodes:
        nodes = hou.selectedNodes()

    for node in nodes:
        company = hou.hda.componentsFromFullNodeTypeName(node.type().name())
        version = company[3]
        node_name = company[2]
        company = company[1].split(":")

        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(DELETE_HDA_BY_NAME, (node_name,))
            hda_id = cursor.fetchone()[0]

            cursor.execute("""SELECT * FROM "Paths" """)
            path_hdas = cursor.fetchall()
            for path_hda in path_hdas:
                if hda_id in path_hda["hdas"]:
                    path_hda["hdas"].remove(hda_id)
                    cursor.execute(UPDATE_PATH,(path_hda["hdas"],path_hda["id"]))


# def create_export_env():
#     """Create export enviorment for the selected node parms to a database"""
#     #create a geo node
#     geo = hou.node("/obj").createNode("geo")
#     geo.setName("export_env")
#     geo.setColor(hou.Color((0, 1, 0)))
#     #create a merge node named DEPENDENCIES and move to good position
#     merge = geo.createNode("merge")
#     merge.setName("DEPENDENCIES", unique_name=True)
#     merge.setColor(hou.Color((1, 0, 1)))
#     merge.moveToGoodPosition(move_outputs=False,move_inputs=False, relative_to_inputs=True)
    
#     #create a null node named OUTPUT
#     output = geo.createNode("null", "OUTPUT")
#     output.setDisplayFlag(True)
#     output.setRenderFlag(True)
#     output.setInput(0, merge)
#     output.setColor(hou.Color((1,0,0)))
#     output.moveToGoodPosition(move_outputs=False,move_inputs=False, relative_to_inputs=True)
    
# def show_node_type():
#     """Show the node type of the selected node"""
#     selected_nodes = hou.selectedNodes()
#     if len(selected_nodes) == 0:
#         hou.ui.displayMessage("Please select a node")
#     elif len(selected_nodes) > 1:
#         hou.ui.displayMessage("Please select only one node")
#     else:
#         hou.ui.displayMessage("The selected node type is {}".format(selected_nodes[0].type().name()))


# def show_node_type():
#     """Show the node name """
#     selected_nodes = hou.selectedNodes()
#     if len(selected_nodes) == 0:
#         hou.ui.displayMessage("Please select a node")
#     elif len(selected_nodes) > 1:
#         hou.ui.displayMessage("Please select only one node")
#     else:
#         hou.ui.displayMessage("The selected node type is {}".format(selected_nodes[0].type().name()))


# #show the node type of all the nodes in the scene
# def show_node_belonging():
#     """Show the selected node name components"""
#     selected_nodes = hou.selectedNodes()
#     if len(selected_nodes) == 0:
#         hou.ui.displayMessage("Please select a node")
#     elif len(selected_nodes) > 1:
#         hou.ui.displayMessage("Please select only one node")
#     else:
#         company = hou.hda.componentsFromFullNodeTypeName(selected_nodes[0].type().name())
#         company = company[1].split(":")
#         hou.ui.displayMessage("The selected node belongs to {}".format(company[0]))

# #Finding all nodes of a specific type
# def find_node_type(node_type):
#     """Find all nodes of a specific type"""
#     all_nodes = hou.sopNodeTypeCategory().nodeTypes(node_type).instances()
    

# def change_node_color():
#     """Change the color of the selected node"""
#     selected_nodes = hou.selectedNodes()
#     if len(selected_nodes) == 0:
#         hou.ui.displayMessage("Please select a node")
#     elif len(selected_nodes) > 1:
#         hou.ui.displayMessage("Please select only one node")
#     else:
#         #open color picker
#         color = hou.ui.selectColor()
#         #change the color of the selected node
#         selected_nodes[0].setColor(color)

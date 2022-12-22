from msilib import init_database
import hou
from hda_register import hda_register
from database import Database, CursorFromConnectionFromPool
from pprint import pprint
import sys
import os

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


def show_node_type():
    """Show the node type of the selected node """
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) == 0:
        hou.ui.displayMessage("Please select a node")
    elif len(selected_nodes) > 1:
        hou.ui.displayMessage("Please select only one node")
    else:
        hou.ui.displayMessage("The selected node type is {}".format(selected_nodes[0].type()))
        pprint(selected_nodes[0].type())


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

def show_node_name():
    """Print the selected node name"""
    selected_node = hou.selectedNodes()
    if len(selected_node) == 0:
        hou.ui.displayMessage("Please select a node")
    elif len(selected_node) > 1:
        hou.ui.displayMessage("Please select only one node")
    else:
        company = hou.hda.componentsFromFullNodeTypeName(selected_node[0].type().name())
        version = company[3]
        node_name = company[2]
        company = company[1].split(":")
        hou.ui.displayMessage("The selected node name is {}".format(node_name))
        pprint(node_name)

def show_node_parms():
    """Show the selected node parms"""
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) == 0:
        hou.ui.displayMessage("Please select a node")
    elif len(selected_nodes) > 1:
        hou.ui.displayMessage("Please select only one node")
    else:
        all_names = []
        for parm in selected_nodes[0].parms():
            all_names.append(parm.name())
        hou.ui.displayMessage("The selected node parms are {}".format(all_names))
        pprint(all_names)
        

def change_node_color():
    """Change the color of the selected node"""
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) == 0:
        hou.ui.displayMessage("Please select a node")
    elif len(selected_nodes) > 1:
        hou.ui.displayMessage("Please select only one node")
    else:
        #open color picker
        color = hou.ui.selectColor()
        #change the color of the selected node
        selected_nodes[0].setColor(color)

def add_quick_material():
    """Add quick material and assign textures"""
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) == 0:
        hou.ui.displayMessage("Please select a node")
    else:
        #select texture folder path
        texture_folder = hou.ui.selectFile(title="Select texture folder", file_type=hou.fileType.Directory)
        # convert $HIP to full path
        texture_folder = hou.expandString(texture_folder)
        missing_textures = []
        for node in selected_nodes:

            #get name form primitive attribute
            try:
                name = node.geometry().prims()[0].attribValue("name")
            except:
                hou.ui.displayMessage("Create a name attribute in primitive attributes for assign textures")
                break

            #create a node in the same position as the selected node
            material_node = node.parent().createNode("quickmaterial")
            #connect the selected node to the material node
            material_node.setInput(0, node)
            #move the material node to good position
            material_node.moveToGoodPosition(move_outputs=False,move_inputs=False, relative_to_inputs=True)

            #set mikkt off
            material_node.parm("usemikkt").set(False)

            #is the texture folder path is not empty
            quick_material_parms = ["principledshader_basecolor_texture_1", 
                                    "principledshader_opaccolor_texture_1", 
                                    "principledshader_baseNormal_texture_1", 
                                    "principledshader_rough_texture_1", 
                                    "principledshader_metallic_texture_1"]

            material_notations =  ["BaseColor", "Opacity", "Normal", "Roughness", "Metallic"]
            for parm in quick_material_parms: 

                texture_name = name + "_" + material_notations[quick_material_parms.index(parm)] + ".jpg"
                texture_full_path = os.path.join(texture_folder, texture_name)

                if os.path.exists(texture_full_path):
                    material_node.parm(parm).set(texture_full_path)                  
                else:
                    missing_textures.append(texture_name)

        if len(missing_textures) > 0:
            #show the missing textures in the console and in the message box
            #For the message box, the list must be converted to string, the brackets must be removed and the list must be listed with \n 
            #For the console, the list must be converted to string with pprint
            pprint(missing_textures)
            missing_textures = str(missing_textures)
            missing_textures = missing_textures.replace("[", "")
            missing_textures = missing_textures.replace("]", "")
            missing_textures = missing_textures.replace("'", "")
            missing_textures = missing_textures.replace(",", "\n")
            hou.ui.displayMessage("The following textures are missing: {}".format(missing_textures))

def switch_quick_material_resulotions():
    """Change the resolution of the quick material nodes"""
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) == 0:
        hou.ui.displayMessage("Please select a node")

    # show the popup window and get the selected resolution from the popup window
    default_selected = (0,)
    resolution = hou.ui.selectFromList(["1024", "2048", "4096"], default_choices=default_selected, exclusive=True, title="Select resolution", message="Select resolution")
    
    selected = (1,)
    if resolution[0] == 0:
        selected = "1k"
    elif resolution[0] == 1:
        selected = "2k"
    elif resolution[0] == 2:
        selected = "4k"
    

    #get all quick material nodes
    selected_nodes = hou.selectedNodes()
    quick_material_nodes = []
    for node in selected_nodes:
        if node.type() == hou.sopNodeTypeCategory().nodeTypes()['labs::quickmaterial::2.2']:
            quick_material_nodes.append(node)

    # change the resolution of the quick material nodes
    for node in quick_material_nodes:
        #get the current texture paths
        quick_material_parms = ["principledshader_basecolor_texture_1", 
                                "principledshader_opaccolor_texture_1", 
                                "principledshader_baseNormal_texture_1", 
                                "principledshader_rough_texture_1", 
                                "principledshader_metallic_texture_1"]
        
        for parm in quick_material_parms:
            #get the current texture path
            texture_path = node.parm(parm).eval()
            #find the current resolution
            if "1k" in texture_path:
                current = "1k"
            elif "2k" in texture_path:
                current = "2k"
            elif "4k" in texture_path:
                current = "4k"
            elif "1K" in texture_path:
                current = "1K"
            elif "2K" in texture_path:
                current = "2K"
            elif "4K" in texture_path:
                current = "4K"
            else:
                # if the texture path does not contain any resolution, skip the texture path
                # show a message box with the texture path

                hou.ui.displayMessage("The texture path does not contain any resolution: {}".format(texture_path)) 
                
                return

            # detect lower case and upper case
            if current.islower():
                selected = selected.lower()
            elif current.isupper():
                selected = selected.upper()


            #change 1k to selected resolution
            texture_path = texture_path.replace(current, selected)
            #set the new texture path
            node.parm(parm).set(texture_path)


def clear_groups_and_attribs():
    """Clear all groups and attribs"""
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) == 0:
        hou.ui.displayMessage("Please select a node")
    else:
        for node in selected_nodes:
            attrib_delete = node.parent().createNode("attribdelete")
            attrib_delete.setInput(0, node)
            attrib_delete.moveToGoodPosition(move_outputs=False,move_inputs=False, relative_to_inputs=True)
            attrib_delete.parm("ptdel").set("*")
            attrib_delete.parm("vtxdel").set("* ^uv ^N")
            attrib_delete.parm("primdel").set("* ^name")
            attrib_delete.parm("dtldel").set("*")

            group_delete = node.parent().createNode("groupdelete")
            group_delete.setInput(0, attrib_delete)
            group_delete.moveToGoodPosition(move_outputs=False,move_inputs=False, relative_to_inputs=True)
            group_delete.parm("group1").set("*")
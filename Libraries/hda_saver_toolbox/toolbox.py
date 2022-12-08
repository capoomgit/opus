from PySide2 import QtWidgets, QtCore, QtGui
import panel_utils
import hou

# A wrapper for button creation
def create_button(text, callback):
    button = QtWidgets.QPushButton(text)
    button.clicked.connect(callback)
    return button

def create_toolbox():

    #create new tabs named export and import in the shelf and add export button to the tab
    tab_widget = QtWidgets.QTabWidget()



    # Create the button inside the tab widget
    export_widget = QtWidgets.QWidget()
    export_layout = QtWidgets.QVBoxLayout()
    export_layout.setAlignment(QtCore.Qt.AlignTop)

    export_layer_button = create_button("Export Layer", panel_utils.save_layer)
    export_layout.addWidget(export_layer_button)

    export_hda_button = create_button("Export Selected HDA's", panel_utils.save_nodes)
    export_layout.addWidget(export_hda_button)

    delete_hdas_button = create_button("Delete Selected HDAAAAAAAAA's", panel_utils.delete_hdas)
    export_layout.addWidget(delete_hdas_button)

    # create_export_env = create_button("Create Export Environment", panel_utils.create_export_env)
    # export_layout.addWidget(create_export_env)

    # show_node_type = create_button("Show Node Type", panel_utils.show_node_type)
    # export_layout.addWidget(show_node_type)

    # show_node_names_components = create_button("Show Nodes Company", panel_utils.show_node_belonging)
    # export_layout.addWidget(show_node_names_components)

    # Add the layout to the root widget
    export_widget.setLayout(export_layout)
    tab_widget.addTab(export_widget, "Export")
    # Utils Layout
    utils_widget = QtWidgets.QWidget()
    utils_layout = QtWidgets.QVBoxLayout()
    utils_layout.setAlignment(QtCore.Qt.AlignTop)

    change_node_color = create_button("Change Node Color", panel_utils.change_node_color)
    utils_layout.addWidget(change_node_color)

    add_quick_material = create_button("Add Quick Material", panel_utils.add_quick_material)
    utils_layout.addWidget(add_quick_material)

    show_node_name = create_button("Show Node Name", panel_utils.show_node_name)
    utils_layout.addWidget(show_node_name)

    show_node_parms = create_button("Show Node Parms", panel_utils.show_node_parms)
    utils_layout.addWidget(show_node_parms)

    clear_groups_and_attrs = create_button("Clear Groups and Attrs", panel_utils.clear_groups_and_attribs)
    utils_layout.addWidget(clear_groups_and_attrs)

    utils_widget.setLayout(utils_layout)
    tab_widget.addTab(utils_widget, "Utils")


    # Return the top-level widget.
    return tab_widget


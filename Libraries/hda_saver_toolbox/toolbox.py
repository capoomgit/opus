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

    # ------------------ Export ------------------

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

    # ------------------ Utils ------------------

    utils_widget = QtWidgets.QWidget()
    utils_layout = QtWidgets.QVBoxLayout()
    utils_layout.setAlignment(QtCore.Qt.AlignTop)

    change_node_color = create_button("Change Node Color", panel_utils.change_node_color)
    utils_layout.addWidget(change_node_color)

    clear_groups_and_attrs = create_button("Clear Groups and Attrs", panel_utils.clear_groups_and_attribs)
    utils_layout.addWidget(clear_groups_and_attrs)

    add_quick_material = create_button("Add Quick Material", panel_utils.add_quick_material)
    utils_layout.addWidget(add_quick_material)

    switch_quick_material_resolutions = create_button("Switch Quick Material Resolutions", panel_utils.switch_quick_material_resulotions)
    utils_layout.addWidget(switch_quick_material_resolutions)

    display_output_node = create_button("Display Output Node", panel_utils.display_output_node)
    utils_layout.addWidget(display_output_node)

    cache_selected_geo_nodes = create_button("Cache Selected Geo Nodes", panel_utils.cache_selected_geo_nodes)
    utils_layout.addWidget(cache_selected_geo_nodes)

    create_object_merge_enviorment = create_button("Create Object Merge Environment", panel_utils.create_object_merge_enviorment)
    utils_layout.addWidget(create_object_merge_enviorment)

    get_input_count = create_button("Get Input Count", panel_utils.get_input_count)
    utils_layout.addWidget(get_input_count)

    utils_widget.setLayout(utils_layout)
    tab_widget.addTab(utils_widget, "Utils")

    # ------------------ Render ------------------

    render_widget = QtWidgets.QWidget()
    render_layout = QtWidgets.QVBoxLayout()
    render_layout.setAlignment(QtCore.Qt.AlignTop)

    # create tab for redshift and mantra
    render_tab_widget = QtWidgets.QTabWidget()

    # ------------------ Mantra ------------------

    mantra_widget = QtWidgets.QWidget()
    mantra_layout = QtWidgets.QVBoxLayout()
    mantra_layout.setAlignment(QtCore.Qt.AlignTop)


    create_mantra_material = create_button("Create Mantra Material", panel_utils.create_mantra_material)
    mantra_layout.addWidget(create_mantra_material)

    create_dome_light_with_hdri = create_button("Create Dome Light With HDRI", panel_utils.create_dome_light_with_hdri)
    mantra_layout.addWidget(create_dome_light_with_hdri)

    create_dome_light_with_sky = create_button("Create Dome Light With Sky", panel_utils.create_dome_light_with_sky)
    mantra_layout.addWidget(create_dome_light_with_sky)

    
    mantra_widget.setLayout(mantra_layout)
    render_tab_widget.addTab(mantra_widget, "Mantra")

    # ------------------ Redshift ------------------

    redshift_widget = QtWidgets.QWidget()
    redshift_layout = QtWidgets.QVBoxLayout()
    redshift_layout.setAlignment(QtCore.Qt.AlignTop)



    create_redshift_material = create_button("Create Redshift Material", panel_utils.create_redshift_material) 
    redshift_layout.addWidget(create_redshift_material)

    create_redshift_dome_light_with_hdri = create_button("Create Redshift Dome Light With HDRI", panel_utils.create_redshift_dome_light_with_hdri)
    redshift_layout.addWidget(create_redshift_dome_light_with_hdri)

    create_redshift_dome_light_with_sky = create_button("Create Redshift Dome Light With Sky", panel_utils.create_redshift_dome_light_with_sky)
    redshift_layout.addWidget(create_redshift_dome_light_with_sky)

    redshift_widget.setLayout(redshift_layout)
    render_tab_widget.addTab(redshift_widget, "Redshift")

    render_layout.addWidget(render_tab_widget)
    render_widget.setLayout(render_layout)
    tab_widget.addTab(render_widget, "Render")

    # ------------------ TOPs ------------------

    tops_widget = QtWidgets.QWidget()
    tops_layout = QtWidgets.QVBoxLayout()
    tops_layout.setAlignment(QtCore.Qt.AlignTop)

    create_wedge_setup_from_switch = create_button("Create Wedge Setup From Switch", panel_utils.create_wedge_setup_from_switch)
    tops_layout.addWidget(create_wedge_setup_from_switch)

    tops_widget.setLayout(tops_layout)
    tab_widget.addTab(tops_widget, "TOPs")


    # ------------------ Development ------------------

    development_widget = QtWidgets.QWidget()
    development_layout = QtWidgets.QVBoxLayout()
    development_layout.setAlignment(QtCore.Qt.AlignTop)

    show_node_name = create_button("Show Node Name", panel_utils.show_node_name)
    development_layout.addWidget(show_node_name)

    show_node_type = create_button("Show Node Type", panel_utils.show_node_type)
    development_layout.addWidget(show_node_type)

    show_node_parms = create_button("Show Node Parms", panel_utils.show_node_parms)
    development_layout.addWidget(show_node_parms)

    development_widget.setLayout(development_layout)
    tab_widget.addTab(development_widget, "Development")


    # Return the top-level widget.
    return tab_widget


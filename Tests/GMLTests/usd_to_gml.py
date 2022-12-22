import os
from lxml import etree
from pxr import Usd, UsdGeom

# Define the input and output file paths
input_path = 'P:\pipeline\standalone_dev\saved\House\Project_1_v0001\Staged\Staged_1_1_0001.usd'
output_path = 'outfile.gml'

# Define the XML namespace URLs as variables
CORE_NS = 'http://www.opengis.net/citygml/2.0'
GML_NS = 'http://www.opengis.net/gml'

# Create the root element of the CityGML file
citygml = etree.Element('{%s}CityModel' % CORE_NS, nsmap={'core': CORE_NS, 'gml': GML_NS})

# Open the USD file and get the root stage
stage = Usd.Stage.Open(input_path)

# Get the list of primitives in the stage
# primitives = stage.GetPseudoRoot().GetAllChildren()

# Iterate over the primitives and extract the mesh data
for primitive in stage.Traverse():
    # Check if the primitive is a mesh
    print(primitive.GetTypeName())
    if primitive.GetTypeName() == "Mesh":
        # Get the vertices and faces of the mesh
        vertices = primitive.GetPoints().GetArray()
        faces = primitive.GetFaceVertexIndices().GetArray()

        # Create a "CityObject" element to represent the building
        building = etree.SubElement(citygml, '{%s}cityObjectMember' % CORE_NS)
        building_object = etree.SubElement(building, '{%s}Building' % CORE_NS)

        # Set the "class" attribute of the object based on the object type
        object_type = primitive.GetName().split('_')[0]  # Extract the object type from the name
        if object_type == 'window':
            building_object.set('class', 'Window')
        elif object_type == 'door':
            building_object.set('class', 'Door')
        else:
            building_object.set('class', 'Other')

        # Add the building's geometry as a "Solid" element
        solid = etree.SubElement(building_object, '{%s}lod1Solid' % CORE_NS)
        exterior = etree.SubElement(solid, '{%s}exterior' % CORE_NS)
        shell = etree.SubElement(exterior, '{%s}CompositeSurface' % CORE_NS)

        # Add the building's faces as "Surface" elements
        for face in faces:
            surface = etree.SubElement(shell, '{%s}surfaceMember' % CORE_NS)
            polygon = etree.SubElement(surface, '{%s}Polygon' % CORE_NS)
            exterior = etree.SubElement(polygon, '{%s}exterior' % CORE_NS)
            ring = etree.SubElement(exterior, '{%s}LinearRing' % CORE_NS)
            for vertex_index in face:

                # Add the vertex as a "pos" element
                pos = etree.SubElement(ring, '{%s}pos' % GML_NS)
                pos.text = ' '.join([str(x) for x in vertices[vertex_index]])

# Write the CityGML file
with open(output_path, 'wb') as f:
    f.write(etree.tostring(citygml, pretty_print=True))
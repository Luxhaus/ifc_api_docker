import json
import ifcopenshell
from app.modules.Rooms import Rooms
from app.modules.Walls import Walls
from app.modules.IFC_Helper import IFC_Helper
import ifcopenshell.geom
file = "app/temp/Testprojekt2.ifc"
rooms = Rooms(file)

model = ifcopenshell.open(file)
#walls = model.by_type("IfcWall")

ifc_helper = IFC_Helper(file)

# extract p_set properties of the first wall
net_side_area = ifc_helper.extract_net_side_area(ifc_helper.walls[0])
#print(net_side_area)

# laufmeter
outer_wall_length = ifc_helper.outer_wall_length(ifc_helper.walls[0])
#print(outer_wall_length)

# laufmeter alle Wände
outer_walls_length = ifc_helper.outer_walls_length()
#print(outer_walls_length)

# benachbarte Wände
adjacent_walls = ifc_helper.get_adjacent_walls(ifc_helper.walls[0])
#print(adjacent_walls)
# print names of the adjacent walls
for wall in adjacent_walls:
    #print(wall.Name)
    pass

# extract IfcSlab
slabs = ifc_helper.get_slabs()
#print(slabs[0])

# extract roof
roofs = ifc_helper.get_roofs()
#print(roofs.__len__())

# extract bodeplatten:
floors = ifc_helper.get_floorings()
print("floors")
print(floors)
print(floors.__len__())

# extract kind of construction


# get_path_elements
path_elements = ifc_helper.get_path_elements(ifc_helper.walls[0])
print("path_elements")
print(path_elements[0])
# get connection coordinates

#get material
material = ifc_helper.get_Material(ifc_helper.walls[0])
#rint("material")
#print(material)

# get connection coordinates
connection_coordinates = ifc_helper.get_connection_coordinates(adjacent_walls[0], adjacent_walls[1])
print("connection_coordinates")
print(connection_coordinates)

# get edges
edges = ifc_helper.find_connected_corners(ifc_helper.walls[0], ifc_helper.walls[1])
print("edges")
print(edges)

#innerwall = ifc_helper.is_corner_near_any_wall_surface(ifc_helper.walls[0], edges["unique_corners_wall2"])
#print("innerwall")
#print(innerwall)

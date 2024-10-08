import json
import ifcopenshell
from app.modules.classes.Rooms import Rooms
from app.modules.classes.Walls import Walls
from app.modules.classes.IFC_Helper import IFC_Helper
from app.modules.classes.Area_Helper import Area_Helper
import ifcopenshell.geom


file = "app/temp/Musterhaus BA (2).ifc"
rooms = Rooms(file)

model = ifcopenshell.open(file)
print(type(model))
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

ah = Area_Helper()

# Hole alle Türen
doors = model.by_type("IfcDoor")
wandstaerke = ah.extract_psetValue(doors[1], "Vollständige Legende", "Wandstärke")
print(wandstaerke)
# extract netto side area of wall
#netto_side_area = ah.extract_netarea(ifc_helper.walls[0])
#print("netto_side_area")
#print(netto_side_area)


for slab in slabs:
    # Filterkriterien:
    if "Mörtelbett" in slab.Name or "Fundament" in slab.Name:
        print(slab.Name)
        # extract netto area of slab
        print("netto_area")
        netto_area = ah.extract_netarea(slab)
        print(netto_area)

        print(ifc_helper.get_mortar_bed_Area())

bad = rooms.get_bathroom()
floor = ah.extract_netarea_floor(bad[0])
print("floor")
print(floor)

def calculate_area(mesh):
    vertices = mesh.verts  # Liste der Vertices
    faces = mesh.faces      # Liste der Indizes, die die Dreiecke beschreiben
    
    area = 0.0
    for i in range(0, len(faces), 3):
        idx1, idx2, idx3 = faces[i], faces[i+1], faces[i+2]
        v1 = vertices[idx1*3:idx1*3+3]
        v2 = vertices[idx2*3:idx2*3+3]
        v3 = vertices[idx3*3:idx3*3+3]

        # Berechnung des Flächeninhalts des Dreiecks über den Kreuzprodukt
        edge1 = [v2[j] - v1[j] for j in range(3)]
        edge2 = [v3[j] - v1[j] for j in range(3)]
        cross_product = [edge1[1]*edge2[2] - edge1[2]*edge2[1],
                        edge1[2]*edge2[0] - edge1[0]*edge2[2],
                        edge1[0]*edge2[1] - edge1[1]*edge2[0]]
        triangle_area = 0.5 * (sum([cross_product[j]**2 for j in range(3)]) ** 0.5)
        area += triangle_area

    return area


# get all walls of the room
#walls = rooms.get_walls_by_geometry(bad[0])
settings = ifcopenshell.geom.settings()
shape = ifcopenshell.geom.create_shape(settings, rooms.get_bathroom()[0])

# Zugriff auf die Mesh-Daten
mesh = shape.geometry

area = calculate_area(mesh) - floor*2
print(f"Die Fläche des Raums beträgt: {area:.2f} Quadratmeter")

# Öffnungen (IfcOpeningElement) identifizieren
openings = model.by_type('IfcOpeningElement')

# Suche nach Öffnungen, die mit einer Wand verknüpft sind, die den Raum umschließt
relevant_openings = []
for opening in openings:
    related_walls = opening.HasFillings  # Öffnungen sind mit Wänden oder anderen Bauteilen verknüpft
    for wall in related_walls:
        print(wall)

# get connected Walls
#walls = ifc_helper.get_Connected_Elements2(ifc_helper.walls[0])

#print("connected walls")
#print(walls)
print("direction info")
count = 0
for wall in ifc_helper.walls:
    #info = ifc_helper.get_Connection_Info(ifc_helper.walls[0], wall)
    #count += 1
    info = ifc_helper.get_direction(wall)
    
    if info is not None:
        pass
        #count += 1
        #print(wall.Name)
        #print(info)
        #print(ifc_helper.get_geometry(wall))
    else:
        #print(wall.Name)
        
        count += 1
        #print("no direction at wall ")
        #print(wall.Name)
    #print(info)
print(count)

# get room of wall
bad = rooms.get_bathroom()
elements = ifc_helper.get_boundaries(bad[0])
print("elements")
print(elements)

# get wall by guid
wall = ifc_helper.get_element_by_guid("1fvJUdD3nFmhMT1oKLY5nC")
print("wall")

#get floors above
floors = ifc_helper.get_floors_above(wall)
print("floors")
walls = model.by_type("IfcWall")
floors = model.by_type("IfcSlab")


geschosse = model.by_type("IfcBuildingStorey")

# Finde das Geschoss, in dem die Wand enthalten ist
contain = wall.ContainedInStructure
print("contain")
print(contain)
if len(contain) > 0:
    relating_structure = contain[0].RelatingStructure
    print("relating_structure")
    print(relating_structure)
    print(geschosse)
    for floor in geschosse:
        if(floor.GlobalId == relating_structure.GlobalId):
        # print level of floor
            print(floor.Name)
            print(floor.Elevation)

# elevation of wall
elevation = ifc_helper.get_elevation(wall)
print("elevation")
print(elevation)


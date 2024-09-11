# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    walls = ifc_file.by_type("IfcWall")
    area_helper = imports.Area_Helper()
    walls_data = []
    data = []
    for wall in walls:
        print(wall)
        type = ifc_file
        walls_data = {
            "name": wall.Name,
            "id": wall.id(),
            "net_area": area_helper.extract_netside_area_wall(wall),
            "type": wall.is_a(),
            "type_identifier": wall.IsTypedBy[0].RelatingType.GlobalId,
            "type_name": wall.IsTypedBy[0].RelatingType.Name
        }
        data.append(walls_data)
    return data
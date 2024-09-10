# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    walls = ifc_file.by_type("IfcWall")
    area_helper = imports.Area_Helper()
    walls_data = []
    data = []
    for wall in walls:
        walls_data = {
            "name": wall.Name,
            "id": wall.id(),
            "net_area": area_helper.extract_netside_area_wall(wall),
        }
        data.append(walls_data)
    return data
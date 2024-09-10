# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    elements = imports.IFC_Helper(ifc_file).get_floorings()
    area_helper = imports.Area_Helper()
    element_data = []
    data = []
    for element in elements:
        element_data = {
            "name": element.Name,
            "id": element.id(),
            "net_area": area_helper.extract_netarea(element),
        }
        data.append(element_data)
    return data
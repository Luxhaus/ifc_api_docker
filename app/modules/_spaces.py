# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    elements = ifc_file.by_type("IfcSpace")
    area_helper = imports.Area_Helper()
    element_data = []
    data = []
    for element in elements:
        element_data = {
            "name": element.LongName,
            "id": element.id(),
            "netarea_floor": area_helper.extract_netarea_floor(element),
        }
        data.append(element_data)
    return data
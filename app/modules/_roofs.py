# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    elements = imports.IFC_Helper(ifc_file).get_roofs()
    area_helper = imports.Area_Helper()
    element_data = []
    data = []
    for element in elements:
        element_data = {
            "name": element.Name,
            "id": element.id(),
            "net_area": area_helper.extract_netarea(element),
            "type": element.is_a(),
            "type_identifier": element.IsTypedBy[0].RelatingType.GlobalId,
            "type_name": element.IsTypedBy[0].RelatingType.Name
        }
        data.append(element_data)
    return data
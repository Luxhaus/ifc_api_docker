# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    elements = ifc_file.by_type("IfcWindow")
    area_helper = imports.Area_Helper()
    _data = []
    data = []
    for element in elements:
        _data = {
            "name": element.Name,
            "id": element.id(),
            "net_area": area_helper.extract_area_window(element),
            "type": element.is_a(),
            "type_identifier": element.IsTypedBy[0].RelatingType.GlobalId,
            "type_name": element.IsTypedBy[0].RelatingType.Name
        }
        data.append(_data)
    return data
# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    area_helper = imports.Area_Helper()
    # get walls
    list = ["IfcWall", "IfcWindow", "IfcRoof", "IfcSlab", "IfcSpace", "IfcDoor"]
    elements = imports.IFC_Helper(ifc_file).get_roofs()
    elements = elements + imports.IFC_Helper(ifc_file).get_floorings()
    print(elements)
    for element in list:
        elements = elements + ifc_file.by_type(element)
    
    _data = []
    data = []
    for element in elements:
        _data = {
            "name": element.Name,
            "id": element.id(),
            "GrossFootprintArea": area_helper.extract_value(element, "GrossFootprintArea"),
            "NetSideArea": area_helper.extract_value(element, "NetSideArea"),
            "GrossSideArea": area_helper.extract_value(element, "GrossSideArea"),
            "GrossArea": area_helper.extract_value(element, "GrossArea"),
            "GrossVolume": area_helper.extract_value(element, "GrossVolume"),
            "Height": area_helper.extract_value(element, "Height"),
            "Width": area_helper.extract_value(element, "Width"),
            "Length": area_helper.extract_value(element, "Length"),
            "NetVolume": area_helper.extract_value(element, "NetVolume"),
            "NetArea": area_helper.extract_value(element, "NetArea"),
            "type": element.is_a(),
  "type_identifier": element.IsTypedBy[0].RelatingType.GlobalId if element.IsTypedBy and len(element.IsTypedBy) > 0 else None,
    "type_name": element.IsTypedBy[0].RelatingType.Name if element.IsTypedBy and len(element.IsTypedBy) > 0 else None
        }
        
        data.append(_data)
    return data
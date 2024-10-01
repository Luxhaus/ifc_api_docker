# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    area_helper = imports.Area_Helper()
    ifc_helper = imports.IFC_Helper(ifc_file)
    # get walls
    list = ["IfcWall", "IfcWindow", "IfcRoof", "IfcSlab", "IfcSpace", "IfcDoor"]
    elements = ifc_helper.get_roofs()
    elements = elements + ifc_helper.get_floorings()
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
            "type_name": element.IsTypedBy[0].RelatingType.Name if element.IsTypedBy and len(element.IsTypedBy) > 0 else None,
            "level" : ifc_helper.get_level(element),
            "elevation": ifc_helper.get_elevation(element),
            "room_name": ifc_helper.get_room_name(element),
            "room_id": ifc_helper.get_room_id(element),
            "is_external": area_helper.extract_CommonPSetValue(element, "IsExternal"),
            "termal_transmittance": area_helper.extract_CommonPSetValue(element, "ThermalTransmittance"),
            "wandstaerke": area_helper.extract_psetValue(element, "Vollständige Legende", "Wandstärke")
        }
        
        data.append(_data)
    return data
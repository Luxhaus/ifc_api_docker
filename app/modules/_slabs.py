# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    # get walls
    slabs = ifc_file.by_type("IfcSlab")
    area_helper = imports.Area_Helper()
    slabs_data = []
    data = []
    for slab in slabs:
        slabs_data = {
            "name": slab.Name,
            "id": slab.id(),
            "net_area": area_helper.extract_netarea(slab),
            "type": slab.is_a(),
            "type_identifier": slab.IsTypedBy[0].RelatingType.GlobalId,
            "type_name": slab.IsTypedBy[0].RelatingType.Name
        }
        data.append(slabs_data)
    return data
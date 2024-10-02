# nicht vergessen die Importe auszukommentieren nach dem Test
from app.modules import imports

def run(ifc_file):
    area_helper = imports.Area_Helper()
    ifc_helper = imports.IFC_Helper(ifc_file)
    project = ifc_file.by_type("IfcProject")

    print(project[0].get_info())
    print(project[0].LongName)
    

    data = {
        "name": project[0].LongName,
        "id": project[0].id(),
        "type_identifier": "IfcProject",
        "type_name": "Project",
        "type": "IfcProject",
    }
        
    return data
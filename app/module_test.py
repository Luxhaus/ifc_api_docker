from app.modules import _read_EasyElements #, _roofs, _walls, _slabs, _floorings, _spaces, _windows, _doors
from app.modules import imports
from app.modules.classes import Area_Helper as ah

file = "app/temp/Musterhaus BA mit Dach.ifc"

ifc_file = imports.ifcopenshell.open(file)

list = []
#list = list + _walls.run(ifc_file)
#list = list + _roofs.run(ifc_file)
#list = list + _slabs.run(ifc_file)
#list = list + _floorings.run(ifc_file)
list = list + _read_EasyElements.run(ifc_file)
print(list)
#print(_walls.run(ifc_file))

#project = ifc_file.by_type("IfcProject")

#print(project[0].get_info())
#get openings

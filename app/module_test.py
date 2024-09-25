from app.modules import _read_EasyElements #, _roofs, _walls, _slabs, _floorings, _spaces, _windows, _doors
from app.modules import imports

file = "app/temp/Musterhaus BA mit Dach.ifc"

ifc_file = imports.ifcopenshell.open(file)

list = []
#list = list + _walls.run(ifc_file)
#list = list + _roofs.run(ifc_file)
#list = list + _slabs.run(ifc_file)
#list = list + _floorings.run(ifc_file)
list = list + _read_EasyElements.run(ifc_file)
print(len(list))
#print(_walls.run(ifc_file))
from app.modules import _roofs, _walls, _slabs, _floorings, _spaces, _windows, _doors
from app.modules import imports

file = "app/temp/Musterhaus BA.ifc"

ifc_file = imports.ifcopenshell.open(file)

list = []
list = list + _walls.run(ifc_file)
list = list + _roofs.run(ifc_file)
list = list + _slabs.run(ifc_file)
list = list + _floorings.run(ifc_file)
print(_doors.run(ifc_file))
#print(list)
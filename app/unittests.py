import unittest
import ifcopenshell
from app.modules.classes.Rooms import Rooms
from app.modules.classes.Walls import Walls
from app.modules.classes.IFC_Helper import IFC_Helper
from app.modules.classes.Area_Helper import Area_Helper
import ifcopenshell.geom
file = "app/temp/Musterhaus BA.ifc"
rooms = Rooms(file)
model = ifcopenshell.open(file)
#walls = model.by_type("IfcWall")

ifc_helper = IFC_Helper(file)
ah = Area_Helper()

class TestStringMethods(unittest.TestCase):
    ## Hole Badezimmer
    def test_get_bathroom(self):
        bathroom = rooms.get_bathroom()
        # wenn bathroom dict is not empty
        self.assertTrue(bathroom)

    def test_bathroom_floor(self):
        bathroom = rooms.get_bathroom()
        floor = ah.extract_netarea_floor(bathroom[0])
        self.assertAlmostEqual(floor, 11.32, places=2)
        
    # ## Außenwandfläche
    # def test_floor(self):
    #     netto_side_area = ifc_helper.extract_net_side_area(ifc_helper.walls[0])
    #     self.assertEqual(netto_side_area, 5353)
    
    # ## Außenwandlänge
    # def test_outer_wall_length(self):

    #     outer_wall_length = ifc_helper.outer_wall_length(ifc_helper.walls[0])
    #     self.assertEqual(outer_wall_length, 0)

    # ## Außenwandlänge aller Wände
    # def test_outer_walls_length(self):
    #     outer_walls_length = ifc_helper.outer_walls_length()
    #     self.assertEqual(outer_walls_length, 0)
    
    # ## benachbarte Wände
    # def test_adjacent_walls(self):
    #     adjacent_walls = ifc_helper.get_adjacent_walls(ifc_helper.walls[0])
    #     self.assertEqual(adjacent_walls, [])


if __name__ == '__main__':
    unittest.main()
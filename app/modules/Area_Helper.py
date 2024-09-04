import ifcopenshell

class Area_Helper:

    def __init__(self) -> None:
        # print typ or class of ifc
        self.ifc = ifcopenshell

    def extract_psetValue(self, element, set_name, parameter_name):
        qtos = self.ifc.util.element.get_psets(element)
        data = qtos[set_name]
        if parameter_name in data:
            return data[parameter_name]
        else:
            return None

    def extract_netside_area_wall(self, wall):
        return self.extract_psetValue(wall, "Qto_WallBaseQuantities", "NetSideArea")
    
    def extract_netarea_slab(self, slab):
        return self.extract_psetValue(slab, "Qto_SlabBaseQuantities", "NetArea")
    
    def extract_netside_area_roof(self, roof):
        pass
    
    def extract_netfloorarea_space(self, space):
        return self.extract_psetValue(space, "Qto_SpaceBaseQuantities", "NetFloorArea")


    def extract_netarea(self, element):

        if(element.is_a("IfcWall")):
            return self.extract_netside_area_wall(element)
        
        elif(element.is_a("IfcSlab")):
            print("Slab")
            return self.extract_netarea_slab(element)
        
        elif(element.is_a("IfcRoof")):
            return self.extract_netside_area_roof(element)
        
    
    def extract_netarea_floor(self, element):
        if(element.is_a("IfcSpace")):
            print(element)
            return self.extract_netfloorarea_space(element)
        
           

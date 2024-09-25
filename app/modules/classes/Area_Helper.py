import ifcopenshell

class Area_Helper:

    def __init__(self) -> None:
        # print typ or class of ifc
        self.ifc = ifcopenshell

    def extract_psetValue(self, element, set_name, parameter_name):
        qtos = self.ifc.util.element.get_psets(element)

        try:
            data = qtos[set_name]
        except KeyError:
            print(f"PropertySet {set_name} not found in {element} (Area_helper.py:extract_psetValue)")
            return None

        if parameter_name in data:
            return data[parameter_name]
        else:
            return None
    
    def extract_value(self, element, value, pset_name=None):
        if pset_name:
            return self.extract_psetValue(element, f"{pset_name}", value)
        return self.extract_psetValue(element, f"Qto_{element.is_a().replace('Ifc', '')}BaseQuantities", value)
    
    def extract_area_window(self, element):
        return self.extract_psetValue(element, "Qto_WindowBaseQuantities", "Area")
    
    def extract_area_door(self, element):
        return self.extract_psetValue(element, "Qto_DoorBaseQuantities", "Area")
    
    # NetsideArea

    def extract_netside_area_wall(self, wall):
        return self.extract_psetValue(wall, "Qto_WallBaseQuantities", "NetSideArea")
    
    def extract_netarea_slab(self, slab):
        return self.extract_psetValue(slab, "Qto_SlabBaseQuantities", "NetArea")
    
    def extract_netside_area_roof(self, roof):
        pass
    
    def extract_netfloorarea_space(self, space):
        return self.extract_psetValue(space, "Qto_SpaceBaseQuantities", "NetFloorArea")

    # Length

    def extract_length_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "Length")
    
    def extract_length_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "Length")
    
    def extract_length_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "Length")
    
    def extract_length_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "Length")
    
    # Height
    
    def extract_height_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "Height")
    
    def extract_height_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "Height")
    
    def extract_height_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "Height")
    
    def extract_height_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "Height")
    
    # Width

    def extract_width_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "Width")
    
    def extract_width_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "Width")
    
    def extract_width_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "Width")
    
    def extract_width_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "Width")
    
    # Volume
    
    def extract_volume_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "Volume")
    
    def extract_volume_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "Volume")
    
    def extract_volume_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "Volume")
    
    def extract_volume_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "Volume")
    
    # GrossSideArea

    def extract_grossside_area_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "GrossSideArea")
    
    def extract_grossside_area_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "GrossSideArea")
    
    def extract_grossside_area_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "GrossSideArea")
    
    def extract_grossside_area_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "GrossSideArea")
    
    # GrossVolume

    def extract_grossvolume_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "GrossVolume")
    
    def extract_grossvolume_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "GrossVolume")
    
    def extract_grossvolume_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "GrossVolume")
    
    def extract_grossvolume_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "GrossVolume")
    
    # NetVolume

    def extract_netvolume_wall(self, element):
        return self.extract_psetValue(element, "Qto_WallBaseQuantities", "NetVolume")
    
    def extract_netvolume_slab(self, element):
        return self.extract_psetValue(element, "Qto_SlabBaseQuantities", "NetVolume")
    
    def extract_netvolume_roof(self, element):
        return self.extract_psetValue(element, "Qto_RoofBaseQuantities", "NetVolume")
    
    def extract_netvolume_floor(self, element):
        return self.extract_psetValue(element, "Qto_FloorBaseQuantities", "NetVolume")
    

    def extract_netarea(self, element):

        if(element.is_a("IfcWall")):
            return self.extract_netside_area_wall(element)
        
        elif(element.is_a("IfcSlab")):
            return self.extract_netarea_slab(element)
        
        elif(element.is_a("IfcRoof")):
            return self.extract_netside_area_roof(element)
        
    
    def extract_netarea_floor(self, element):
        if(element.is_a("IfcSpace")):
            print(element)
            return self.extract_netfloorarea_space(element)
        
    def extract_length(self, element):
        if(element.is_a("IfcWall")):
            return self.extract_length_wall(element)
        
        elif(element.is_a("IfcSlab")):
            return self.extract_length_slab(element)
        
        elif(element.is_a("IfcRoof")):
            return self.extract_length_roof(element)
        
        elif(element.is_a("IfcFloor")):
            return self.extract_length_floor(element)
        
    def extract_height(self, element):
        if(element.is_a("IfcWall")):
            return self.extract_height_wall(element)
        
        elif(element.is_a("IfcSlab")):
            return self.extract_height_slab(element)
        
        elif(element.is_a("IfcRoof")):
            return self.extract_height_roof(element)
        
        elif(element.is_a("IfcFloor")):
            return self.extract_height_floor(element)
        
    def extract_width(self, element):
        if(element.is_a("IfcWall")):
            return self.extract_width_wall(element)
        
        elif(element.is_a("IfcSlab")):
            return self.extract_width_slab(element)
        
        elif(element.is_a("IfcRoof")):
            return self.extract_width_roof(element)
        
        elif(element.is_a("IfcFloor")):
            return self.extract_width_floor(element)
        
    def extract_volume(self, element):
        if(element.is_a("IfcWall")):
            return self.extract_volume_wall(element)
        
        elif(element.is_a("IfcSlab")):
            return self.extract_volume_slab(element)
        
        elif(element.is_a("IfcRoof")):
            return self.extract_volume_roof(element)
        
        elif(element.is_a("IfcFloor")):
            return self.extract_volume_floor(element)
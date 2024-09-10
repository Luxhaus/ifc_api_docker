import ifcopenshell
import json
from app.modules.classes.Area_Helper import Area_Helper

class Walls:
    def __init__(self, file):
        self.ifc_file = ifcopenshell.open(file)
        self.walls = self.ifc_file.by_type("IfcWall")
        self.walls_data = []
        self.area_helper = Area_Helper()
    
    def extract_properties(self, element):
        properties = {}
        if hasattr(element, "IsDefinedBy"):
            for definition in element.IsDefinedBy:
                if definition.is_a("IfcRelDefinesByProperties"):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a("IfcPropertySet"):
                        for prop in property_set.HasProperties:
                            if prop.is_a("IfcProperty"):  # Handle both single and set-valued properties
                                self.extract_property_value(prop, properties)

        return properties

    def extract_property_value(self, property, properties):
        if property.is_a("IfcPropertySingleValue"):
            properties[property.Name] = property.NominalValue.wrappedValue
        elif property.is_a("IfcPropertySet"):
            for prop in property.HasProperties:
                self.extract_property_value(prop, properties)  # Recursively handle nested property sets
        elif property.is_a("IfcPropertyList"):
            values = []
            for item in property.Items:
                if item.is_a("IfcValue"):
                    values.append(item.wrappedValue)
            if values:
                properties[property.Name] = values
        else:
            # Handle other property types (e.g., IfcPropertyEnumeratedValue) as needed
            pass
    
    def get_coverings(self, wall):
        coverings = []
        for rel in self.ifc_file.by_type('IfcRelCoversBldgElements'):
            if rel.RelatingBuildingElement == wall:
                for covering in rel.RelatedCoverings:
                    coverings.append({
                        "type": covering.is_a(),
                        "name": covering.Name,
                        "properties": self.extract_properties(covering),
                        "area_sqm": self.extract_area(covering)
                    })
        return coverings
    
    def extractOuterArea(self, wall):
        for prop in wall.IsDefinedBy:
            if prop.is_a('IfcRelDefinesByProperties'):
                prop_set = prop.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityArea'):
                            return quantity.AreaValue.wrappedValue
        return None
    
    def extractInnerArea(self, wall):
        for prop in wall.IsDefinedBy:
            if prop.is_a('IfcRelDefinesByProperties'):
                prop_set = prop.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityArea') and quantity.Name == "GrossArea":
                            return quantity.AreaValue
        return None
    
    def get_Connected_Walls(self, wall):
        connected_walls = []
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == wall:
                connected_walls.append(rel.RelatedElement)
        return connected_walls
                
    def exportAsJson(self):
        self.walls_data = []
        for wall in self.walls:
            walls_data = {
                "name": wall.Name,
                "net_area": self.area_helper.extract_netside_area_wall(wall),
            }
            self.walls_data.append(walls_data)
            print(walls_data)
        return json.dumps(self.walls_data, indent=4)
    
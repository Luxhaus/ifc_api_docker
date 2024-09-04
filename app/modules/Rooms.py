import ifcopenshell
import ifcopenshell.geom
import json

class Rooms:
    def __init__(self, file):
        self.ifc_file = ifcopenshell.open(file)
        self.spaces = self.ifc_file.by_type("IfcSpace")
        self.spaces_data = []
    
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
    
    def get_coverings(self, space):
        coverings = []
        for rel in self.ifc_file.by_type('IfcRelCoversSpaces'):
            if rel.RelatingSpace == space:
                for covering in rel.RelatedCoverings:
                    coverings.append({
                        "type": covering.is_a(),
                        "name": covering.Name,
                        "properties": self.extract_properties(covering),
                        "area_sqm": self.extract_area(covering)
                    })
        return coverings
    
    def extract_area(self, covering):
        # Hier eine vereinfachte Annahme, dass die Fläche in den Eigenschaften zu finden ist
        # In der Praxis kann dies komplexer sein und eine echte geometrische Berechnung erfordern
        for prop in covering.IsDefinedBy:
            if prop.is_a('IfcRelDefinesByProperties'):
                prop_set = prop.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityArea') and quantity.Name == "GrossArea":
                            return quantity.AreaValue
        return None

    def get_openings(self, space):
        openings = []
        for rel in self.ifc_file.by_type('IfcRelVoidsElement'):
            if rel.RelatingBuildingElement in space.ContainsElements:
                for opening in rel.RelatedOpeningElement.HasFillings:
                    element = opening.RelatedBuildingElement
                    if element.is_a('IfcDoor') or element.is_a('IfcWindow'):
                        openings.append({
                            "type": element.is_a(),
                            "name": element.Name,
                            "properties": self.extract_properties(element)
                        })
        return openings

    def get_contained_elements(self, space):
        contained_elements = []
        for rel in self.ifc_file.by_type('IfcRelContainedInSpatialStructure'):
            if rel.RelatingStructure == space:
                for element in rel.RelatedElements:
                    if not element.is_a('IfcCovering') and not element.is_a('IfcDoor') and not element.is_a('IfcWindow'):
                        contained_elements.append({
                            "type": element.is_a(),
                            "name": element.Name,
                            "properties": self.extract_properties(element)
                        })
        return contained_elements
    
    def get_bathroom(self):
        bathrooms = []
        for space in self.spaces:
            if "Bad" in space.LongName:
                bathrooms.append(space)
        return bathrooms

    def exportAsJson(self):
        self.space_data = []

        for space in self.spaces:
            space_data = {
                "name": space.Name,
                "properties": self.extract_properties(space),
                "contained_elements": self.get_contained_elements(space),
                "coverings": self.get_coverings(space),  # Fliesen als IfcCovering
                "openings": self.get_openings(space)  # Türen und Fenster
            }
            self.spaces_data.append(space_data)

        # In JSON konvertieren
        return json.dumps(self.spaces_data, indent=4)
    
    def get_room_floor(self, space):
        for slab in self.ifc_file.by_type("IfcSlab"):
            for rel in slab.HasAssociations:
                print(rel)
                #if rel.RelatingObject == space:
                #    return slab
    
    def get_walls(self, space):
        walls = []
        for rel in self.ifc_file.by_type('IfcRelSpaceBoundary'):
            if rel.RelatingSpace == space:
                walls.append({
                    "type": rel.RelatedBuildingElement.is_a(),
                    "name": rel.RelatedBuildingElement.Name,
                    "properties": self.extract_properties(rel.RelatedBuildingElement)
                })
        return walls
    
    def is_within_or_intersects(bbox1, bbox2):
        # Prüfe auf Überlappung der Bounding Boxes
        return not (bbox1.max.x < bbox2.min.x or
                    bbox1.min.x > bbox2.max.x or
                    bbox1.max.y < bbox2.min.y or
                    bbox1.min.y > bbox2.max.y or
                    bbox1.max.z < bbox2.min.z or
                    bbox1.min.z > bbox2.max.z)
    
    def get_walls_by_geometry(self, space):
        # Schleife durch alle Wände und prüfe die räumliche Beziehung
        space_bbox = ifcopenshell.geom.bounding_box(space)
        walls = self.ifc_file.by_type("IfcWall")
        for wall in walls:
            wall_bbox = ifcopenshell.geom.bounding_box(wall)
            if self.is_within_or_intersects(space_bbox, wall_bbox):
                print(f"Wall ID {wall.id()} encloses the space")
                # Weitere Verarbeitung der Wandflächen



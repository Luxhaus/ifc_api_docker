import ifcopenshell
import json
import shapely
import ifcopenshell.geom
import numpy as np



class IFC_Helper:

    def __init__(self, file) -> None:
        if isinstance(file, ifcopenshell.file):
            self.ifc_file = file
        else:
            self.ifc_file = ifcopenshell.open(file)
        self.file = file
        self.spaces = self.ifc_file.by_type("IfcSpace")
        self.walls = self.ifc_file.by_type("IfcWall")
        self.settings = ifcopenshell.geom.settings()
        
        return None
    
    def extract_net_side_area(self, wall):
        wall_type_qtos = ifcopenshell.util.element.get_psets(wall)
        data = wall_type_qtos["Qto_WallBaseQuantities"]
        #print(data)
        if 'NetSideArea' in data:
            return data['NetSideArea']
        else:
            return None
        
    # einheit für die Flächenberechnung
    def get_area_unit(self):
        area_unit = None
        for unit in self.ifc_file.by_type("IfcUnitAssignment"):
            for unit_set in unit.Units:
                if unit_set.is_a("IfcSIUnit"):
                    if unit_set.UnitType == "AREAUNIT":
                        area_unit = unit_set
        return area_unit
    
    # extract Außenwände in laufmetern
    def outer_wall_length(self, wall):
        wall_type_qtos = ifcopenshell.util.element.get_psets(wall)
        data = wall_type_qtos["Qto_WallBaseQuantities"]
        if 'Length' in data:
            return data['Length']
        else:
            return None
        
    def outer_walls_length(self):
        length = 0
        for wall in self.walls:
            length += self.outer_wall_length(wall)
        return length
    
    # finde für eine Außenwand, die berührenden Wände
    def get_adjacent_walls(self, wall):
        adjacent_walls = []
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == wall:
                if rel.RelatedElement.is_a('IfcWall'):
                    adjacent_walls.append(rel.RelatedElement)
        return adjacent_walls
    
    def get_ConnectionType(self, wall1, wall2):
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == wall1 and rel.RelatedElement == wall2:
                print(rel)
                return rel.ConnectionType
        return None
            

    # extract IfcSlab
    def get_slabs(self):
        slabs = self.ifc_file.by_type("IfcSlab")
        return slabs
    
    # extract bodenplatte
    def get_floorings(self):
            """Extrahiert alle Bodenplatten aus dem IFC-Modell.

            Args:
                self: Eine Instanz der Klasse, die auf das IFC-Modell zugreift.

            Returns:
                Liste: Eine Liste von IfcSlab-Elementen, die als Bodenplatten identifiziert wurden.
            """

            all_slabs = self.ifc_file.by_type("IfcSlab")
            floor_slabs = []

            for slab in all_slabs:
                # Filterkriterien:
                if "Bodenplatte" in slab.Name or "Fundament" in slab.Name:
                    floor_slabs.append(slab)
                elif "Pset_Floor" in slab.IsDefinedBy:
                    floor_slabs.append(slab)
                elif "FLOOR" in slab.PredefinedType:
                    floor_slabs.append(slab)
                elif ".FLOOR." in slab.Name:
                    floor_slabs.append(slab)

            return floor_slabs

    # extract IfcRoof
    def get_roofs(self):
        roofs = self.ifc_file.by_type("IfcRoof")
        return roofs
    
    # take a wall and extract IfcRelConnectsPathElements
    def get_path_elements(self, wall):
        path_elements = []
        for rel in self.ifc_file.by_type('IfcRelConnectsPathElements'):
            print(rel)
            if rel.RelatingElement == wall:
                path_elements.append(rel.RelatedElement)
        return path_elements
    
    def get_Material(self, element):
        material = ifcopenshell.util.element.get_material(element)
        parts = ifcopenshell.util.element.get_parts(element)
        #print(parts)

        return material
    
    def get_connection_coordinates(self, wall1, wall2):
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == wall1 and rel.RelatedElement == wall2:
                return rel.ConnectionGeometry
        return None
  
    #get IfcRelContainedInSpatialStructure
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
    
    # freie Bodenfläche bestimmen erstmal für die erste ebene, später dann für einzelne Räume
    def get_free_floor_area(self):
        free_floor_area = 0
        for slab in self.get_floorings():
            area = self.extract_area(slab)
            free_floor_area += area
        return free_floor_area
    
    # extract sub elements of a wall
    def get_geometry(self, element):
        return ifcopenshell.geom.create_shape(self.settings, element)
        
    def get_wall_corners(self, wall):

        # Geometrie der Wand erstellen
        shape = ifcopenshell.geom.create_shape(self.settings, wall)
        geometry = shape.geometry

        vertices = geometry.verts
        faces = geometry.faces

        # Eckpunkte der Wand sammeln
        corners = set()
        for i in range(0, len(faces), 3):
            corner_1 = tuple(vertices[faces[i] * 3:faces[i] * 3 + 3])
            corner_2 = tuple(vertices[faces[i+1] * 3:faces[i+1] * 3 + 3])
            corner_3 = tuple(vertices[faces[i+2] * 3:faces[i+2] * 3 + 3])

            corners.add(corner_1)
            corners.add(corner_2)
            corners.add(corner_3)
        
        return corners

    def find_connected_corners(self, wall1, wall2, tolerance=1e-6):
        # Ecken der beiden Wände extrahieren
        corners_wall1 = self.get_wall_corners(wall1)
        corners_wall2 = self.get_wall_corners(wall2)

        connected_corners = set()

        # Gemeinsame Ecken identifizieren, die innerhalb der Toleranz verbunden sind
        for corner1 in corners_wall1:
            for corner2 in corners_wall2:
                if self.are_corners_connected(corner1, corner2, tolerance):
                    connected_corners.add(corner1)
                    connected_corners.add(corner2)

        # Unverbundene Ecken jeder Wand finden
        unique_corners_wall1 = corners_wall1 - connected_corners
        unique_corners_wall2 = corners_wall2 - connected_corners

        return {
            "connected_corners": connected_corners,
            "unique_corners_wall1": unique_corners_wall1,
            "unique_corners_wall2": unique_corners_wall2
        }

    def are_corners_connected(self, corner1, corner2, tolerance):
        # Überprüft, ob zwei Ecken innerhalb der Toleranz verbunden sind
        return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(corner1, corner2))
    
    # check if a point is inside a wall
    def is_point_inside_wall(self, wall, point):
        # Geometrie der Wand erstellen
        shape = ifcopenshell.geom.create_shape(self.settings, wall)
        geometry = shape.geometry

        vertices = geometry.verts
        faces = geometry.faces

        # Ebenengleichung der Wand berechnen
        normal = geometry.face_normals[0]
        d = -sum(normal[i] * vertices[faces[0] * 3 + i] for i in range(3))

        # Punkt in die Ebenengleichung einsetzen
        point_distance = sum(normal[i] * point[i] for i in range(3)) + d

        return point_distance < 0
    
    def calculate_face_normal(self, vertices, face):
        # Extrahiere die Ecken der Fläche
        p1 = np.array(vertices[face[0] * 3: face[0] * 3 + 3])
        p2 = np.array(vertices[face[1] * 3: face[1] * 3 + 3])
        p3 = np.array(vertices[face[2] * 3: face[2] * 3 + 3])

        # Vektoren entlang der Fläche berechnen
        v1 = p2 - p1
        v2 = p3 - p1

        # Normale der Fläche berechnen (Kreuzprodukt)
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)  # Normieren der Normalen

        return normal

    def is_corner_near_any_wall_surface(self, wall, corner, tolerance=1e-6):
        # Geometrie der Wand erstellen
        shape = ifcopenshell.geom.create_shape(self.settings, wall)
        geometry = shape.geometry

        vertices = geometry.verts
        faces = geometry.faces
        normals = geometry.normals if hasattr(geometry, 'normals') else []

        for i, face in enumerate(faces):
            # Berechne die Normale, falls normals nicht verfügbar sind
            if not normals or len(normals) < len(faces):
                normal = self.calculate_face_normal(vertices, face)
            else:
                normal = np.array(normals[i])
            
            # Berechne den Offset d der Ebene
            p1 = np.array(vertices[face[0] * 3: face[0] * 3 + 3])
            d = -np.dot(normal, p1)

            # Berechne den Abstand der Ecke zur Fläche
            point = np.array(corner)
            point_distance = np.dot(normal, point) + d
            point_distance = abs(point_distance) / np.linalg.norm(normal)  # Abstand zur Normale

            if point_distance <= tolerance:
                return True

        return False
    
    #mörtelbett auslesen
    def get_mortar_bed(self):
        all_slabs = self.ifc_file.by_type("IfcSlab")
        floor_slabs = []

        for slab in all_slabs:
            # Filterkriterien:
            if "Mörtelbett" in slab.Name or "Fundament" in slab.Name:
                floor_slabs.append(slab)
        return floor_slabs
    
    def get_mortar_bed_Volume(self):
        mortar_bed = self.get_mortar_bed()
        for slab in mortar_bed:
            wall_type_qtos = ifcopenshell.util.element.get_psets(slab)
            data = wall_type_qtos["Qto_SlabBaseQuantities"]
            if 'NetVolume' in data:
                return data['NetVolume']
    
    def get_mortar_bed_Area(self):
        mortar_bed = self.get_mortar_bed()
        for slab in mortar_bed:
            wall_type_qtos = ifcopenshell.util.element.get_psets(slab)
            data = wall_type_qtos["Qto_SlabBaseQuantities"]
            if 'NetArea' in data:
                return data['NetArea']
    
    def get_Connected_Elements(self, element):
        connected_elements = []
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == element:
                connected_elements.append(rel.RelatedElement)
        return connected_elements
    
    def get_Connection_Info2(self, wall1, wall2):
        connections = []
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == wall1 and rel.RelatedElement == wall2:
                connections.append(rel)
        return rel
            

    def get_Connection_Info(self, wall1, wall2):
        connections = []
        # Sammle alle Verbindungen zwischen den Wänden
        for rel in self.ifc_file.by_type('IfcRelConnectsElements'):
            if rel.RelatingElement == wall1 and rel.RelatedElement == wall2:
                connections.append(rel)

        # Falls eine Verbindung gefunden wurde, gib die Platzierungsinformationen der Wände aus
        if connections:
            # Wand 1: Platzierungsdaten abrufen
            direction_wall1 = self.get_direction(wall1)
            direction_wall2 = self.get_direction(wall2)
            
            # Informationen über die Platzierung und Orientierung der Wände ausgeben
            
            #wall1info = [f"Wand 1 Position: {location_wall1}, Achse: {axis_wall1}, Richtung: {ref_direction_wall1}"]
            #wall2info = [f"Wand 2 Position: {location_wall2}, Achse: {axis_wall2}, Richtung: {ref_direction_wall2}"]

            # Berechnung der Winkel zwischen den Wänden
            
        else:
            print("Keine Verbindung zwischen den Wänden gefunden.")
        
        return [connections, direction_wall1, direction_wall2]

        
    def get_geo(self, wall):
        # Extrahiere die Richtung der Wand
        placement = wall.ObjectPlacement
        if placement and hasattr(placement, 'RelativePlacement'):
            location_wall1 = placement.RelativePlacement.Location
            axis_wall1 = placement.RelativePlacement.Axis if hasattr(placement.RelativePlacement, 'Axis') else None
            ref_direction_wall1 = placement.RelativePlacement.RefDirection if hasattr(placement.RelativePlacement, 'RefDirection') else None
            return location_wall1, axis_wall1, ref_direction_wall1
        return None
    
    def get_direction(self, wall):
        # Extrahiere die Richtung der Wand
        placement = wall.ObjectPlacement
        if placement and hasattr(placement, 'RelativePlacement'):
            if hasattr(placement.RelativePlacement, 'RefDirection'):
                return placement.RelativePlacement.RefDirection 
            else:
                return None
           
        return None
    
    def get_boundaries(self, room):
        boundaries = []
        for rel in self.ifc_file.by_type('IfcRelSpaceBoundary'):
            if rel.RelatingSpace.GlobalId == room.GlobalId:
                #        print(rel.RelatedBuildingElement.Name)
                #        print(rel.InternalOrExternalBoundary)
                #        print(rel.PhysicalOrVirtualBoundary)
                #        print(rel.ConnectionGeometry)
                boundaries.append(rel.RelatedBuildingElement)
        return boundaries

    def get_element_by_guid(self, guid):
        element = self.ifc_file.by_guid(guid)
        return element
    
    # überarbeiten
    def get_floors_above(self, element):
        floors = []
        for rel in self.ifc_file.by_type('IfcRelContainedInSpatialStructure'):
            if rel.RelatedElements[0] == element:
                for floor in rel.RelatingStructure.ContainsElements:
                    floors.append(floor)
        return floors
    
    def get_elevation(self, element):
        for rel in self.ifc_file.by_type('IfcRelContainedInSpatialStructure'):
            if element in rel.RelatedElements:
                return rel.RelatingStructure.Elevation
        return None
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
    
    def extract_CommonPSetValue(self, element, value, pset_name=None):
        if pset_name:
            return self.extract_psetValue(element, f"{pset_name}", value)
        return self.extract_psetValue(element, f"Pset_{element.is_a().replace('Ifc', '')}Common", value)
    
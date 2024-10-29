import xml.etree.ElementTree as ET
from .components import Window, Button

def parse_ui(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return parse_element(root)

def parse_element(element):
    if element.tag == "window":
        window = Window(
            title=element.attrib.get("title"),
            width=int(element.attrib.get("width", 800)),
            height=int(element.attrib.get("height", 600)),
        )
        for child in element:
            window.add_child(parse_element(child))
        return window

    elif element.tag == "button":
        return Button(
            text=element.attrib.get("text"),
            id=element.attrib.get("id")
        )
        
    elif element.tag == "inputpanel":
        return InputPanel(
            value=element.attrib.get("value", ""),
            id=element.attrib.get("id")
        )
        
    else:
        raise ValueError(f"Неизвестный элемент: {element.tag}")
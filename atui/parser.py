import xml.etree.ElementTree as ET

def window_create(file):
    tree = ET.parse(file)
    root = tree.getroot()
    
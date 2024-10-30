class CSSStyle:
    def __init__(self):
        self.styles = {}

    def set_property(self, property_name, value):
        self.styles[property_name] = value

    def get_property(self, property_name):
        return self.styles.get(property_name)

    def __str__(self):
        return str(self.styles)

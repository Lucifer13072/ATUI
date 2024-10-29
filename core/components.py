class Component:
    def __init__(self, **attributes):
        self.attributes = attributes
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def render(self):
        raise NotImplementedError

class Button(Component):
    def __init__(self, text, **attributes):
        super().__init__(**attributes)
        self.text = text

    def render(self):
        return f"Button: {self.text}, Attributes: {self.attributes}"

class Window(Component):
    def __init__(self, title, width, height, **attributes):
        super().__init__(**attributes)
        self.title = title
        self.width = width
        self.height = height

    def render(self):
        rendered_children = [child.render() for child in self.children]
        return f"Window: {self.title} ({self.width}x{self.height})\n" + "\n".join(rendered_children)

class InputPanel(Component):
    def __init__(self, value="", **attributes):
        super().__init__(**attributes)
        self.value = value

    def render(self):
        return f"InputPanel: {self.value}, Attributes: {self.attributes}"
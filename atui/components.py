from .styles import CSSStyle

class Component:
    def __init__(self, style=None, **attributes):
        self.attributes = attributes
        self.children = []
        self.style = style if style else CSSStyle()

    def add_child(self, child):
        """Добавляет дочерний компонент."""
        self.children.append(child)

    def render(self):
        """Метод рендеринга компонента, должен быть переопределен в подклассах."""
        raise NotImplementedError


class Button(Component):
    def __init__(self, text, style=None, **attributes):
        super().__init__(style, **attributes)
        self.text = text

    def render(self):
        """Рендерит кнопку."""
        return f"Button: {self.text}, Attributes: {self.attributes}, Styles: {self.style.render()}"


class Window(Component):
    def __init__(self, title, width, height, style=None, **attributes):
        super().__init__(style, **attributes)
        self.title = title
        self.width = width
        self.height = height

    def render(self):
        """Рендерит окно с дочерними компонентами."""
        rendered_children = [child.render() for child in self.children]
        return f"Window: {self.title} ({self.width}x{self.height})\n" + "\n".join(rendered_children)


class InputPanel(Component):
    def __init__(self, value="", style=None, **attributes):
        super().__init__(style, **attributes)
        self.value = value

    def render(self):
        """Рендерит панель ввода."""
        return f"InputPanel: {self.value}, Attributes: {self.attributes}, Styles: {self.style.render()}"

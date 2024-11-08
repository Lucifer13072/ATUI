from .styles import CSSStyle

class Component:
    def __init__(self, style=None, **attributes):
        self.attributes = attributes  # Атрибуты компонента (например, id, классы)
        self.children = []  # Дочерние компоненты
        self.style = style if style else CSSStyle()  # Стиль компонента

    def add_child(self, child):
        """Добавляет дочерний компонент."""
        self.children.append(child)

    def render(self):
        """Метод рендеринга компонента, должен быть переопределен в подклассах."""
        raise NotImplementedError

    def render_styles(self):
        """Рендерит стили компонента"""
        return self.style.render()

    def render_children(self):
        """Рендерит дочерние компоненты"""
        return [child.render() for child in self.children]


class Button(Component):
    def __init__(self, text, position=(0, 0), size=(100, 30), command=None, style=None, **attributes):
        super().__init__(style, **attributes)
        self.text = text
        self.position = position
        self.size = size
        self.command = command  # Может быть функцией, которая выполняется при клике

    def render(self):
        """Рендерит кнопку."""
        # Здесь вы можете интегрировать рендеринг в вашу графическую систему, например, создание окна с кнопкой
        style = self.render_styles()
        return f"Button: {self.text}, Position: {self.position}, Size: {self.size}, Attributes: {self.attributes}, Styles: {style}"


class InputPanel(Component):
    def __init__(self, value="", position=(0, 0), size=(200, 30), style=None, **attributes):
        super().__init__(style, **attributes)
        self.value = value
        self.position = position
        self.size = size

    def render(self):
        """Рендерит панель ввода."""
        style = self.render_styles()
        return f"InputPanel: {self.value}, Position: {self.position}, Size: {self.size}, Attributes: {self.attributes}, Styles: {style}"


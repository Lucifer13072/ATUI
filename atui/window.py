from .graphics import Graphics  # Импортируем класс Graphics

class Window:
    def __init__(self, title="Window", width=800, height=600):
        self.title = title
        self.graphics = Graphics(width, height)

    def render(self):
        self.graphics.show()  # Отображаем окно


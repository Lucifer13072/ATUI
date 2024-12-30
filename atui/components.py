from .grafics import generate

class Components:
    def __init__(self, width, height, shadow, background_color):
        self.width = width
        self.height = height
        self.shadow = shadow
        self.background_color = background_color
    
    def render(self):
        # Базовый метод render может быть переопределён
        pass

class Window:
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name  # Имя окна
    
    def render(self):
        generate(width=self.width, heigth=self.height, name=self.name)
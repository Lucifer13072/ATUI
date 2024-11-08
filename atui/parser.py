import xml.etree.ElementTree as ET
from atui.components import Button, InputPanel
from atui.window import Window

class Parser:
    def parse_ui_file(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        components = []
        if root.tag == "window":
            # Извлекаем атрибуты окна
            title = root.attrib.get("title", "Окно")
            width = int(root.attrib.get("width", 800))
            height = int(root.attrib.get("height", 600))
            
            # Создаем окно
            window = Window(title, width, height)
            
            # Обрабатываем дочерние элементы окна
            for element in root:
                if element.tag == "button":
                    button = self.create_button(element)
                    window.add_component(button)  # Добавляем компонент в окно
                elif element.tag == "textField":
                    text_field = self.create_text_field(element)
                    window.add_component(text_field)  # Добавляем компонент в окно
            
            return window
        else:
            raise ValueError("Root element must be 'window'.")

    def create_button(self, element):
        # Извлекаем атрибуты кнопки
        text = element.attrib.get("text", "Кнопка")
        position = tuple(map(int, element.attrib.get("position", "0,0").split(',')))
        size = tuple(map(int, element.attrib.get("size", "100,30").split(',')))
        command = element.attrib.get("onclick", None)
        
        # Если есть обработчик события, передаем его
        if command:
            # В реальной ситуации мы бы передавали функцию/метод для обработки события
            command = self.get_command_function(command)
        
        return Button(position, size, text, command)

    def create_text_field(self, element):
        # Извлекаем атрибуты текстового поля
        position = tuple(map(int, element.attrib.get("position", "0,0").split(',')))
        size = tuple(map(int, element.attrib.get("size", "200,30").split(',')))
        return InputPanel(position, size)

    def get_command_function(self, command_str):
        # В реальной реализации это должно быть привязано к методу
        # Пример: В Python это может быть что-то типа eval или использование функций по имени
        print(f"Command received: {command_str}")
        # Для простоты, просто вернем команду как строку или вызовем её как функцию
        return lambda: print(f"Executed command: {command_str}")

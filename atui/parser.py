import re
from .components import Button, InputPanel 

class Parser:
    def parse(self, markup):
        components = []
        # Ищем окно
        window_match = re.search(r'<window.*?>(.*?)</window>', markup, re.DOTALL)
        if window_match:
            # Получаем содержимое окна
            body = window_match.group(1)
            component_matches = re.findall(r'<(.*?)\s*\/?>', body)
            for match in component_matches:
                tag, attrs = self.parse_tag(match)
                if tag == 'button':
                    components.append(self.create_button(attrs))
                elif tag == 'textField':
                    components.append(self.create_text_field(attrs))
        return components

    def parse_tag(self, tag_str):
        parts = tag_str.split()
        tag = parts[0]
        attrs = {}
        for part in parts[1:]:
            key_value = part.split('=')
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1].strip('"')  # Убираем кавычки
                attrs[key] = value
        return tag, attrs

    def create_button(self, attrs):
        # Извлекаем атрибуты кнопки
        text = attrs.get('text', 'Кнопка')
        position = tuple(map(int, attrs.get('position', '0,0').split(',')))
        size = tuple(map(int, attrs.get('size', '100,30').split(',')))
        command = attrs.get('onclick', None)
        return Button(position, size, text, command)

    def create_text_field(self, attrs):
        # Извлекаем атрибуты текстового поля
        position = tuple(map(int, attrs.get('position', '0,0').split(',')))
        size = tuple(map(int, attrs.get('size', '200,30').split(',')))
        return InputPanel(position, size)

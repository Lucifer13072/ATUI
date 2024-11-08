from atui.parser import Parser

parser = Parser()

# Указываем путь к файлу .ui
window = parser.parse_ui_file("inter.ui")

# Создаём и отображаем окно
window.create()
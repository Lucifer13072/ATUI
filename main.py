from atui.window import Window  # Импортируем класс Window

if __name__ == "__main__":
    window = Window("Мое Окно", 800, 600)  # Создаем окно с заданным заголовком и размерами
    window.render()  # Отображаем окно

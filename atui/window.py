from .graphics import create_window, register_window_class
import ctypes
import ctypes.wintypes


class Window:
    def __init__(self, title="Window", width=800, height=600):
        self.title = title
        self.width = width
        self.height = height
        self.hwnd = None
        self.components = []  # Список компонентов окна

    def create(self):
        wndclass = register_window_class()
        self.hwnd = create_window(wndclass, self.width, self.height, self.title)
        msg = ctypes.wintypes.MSG()
        while True:
            result = ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)
            if result == 0:  # WM_QUIT
                break  # Завершаем цикл
            
            # Обработка других сообщений
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

    def render(self):
        if self.hwnd is not None:
            # Логика рендеринга компонентов (например, кнопок, текста) здесь
            for component in self.components:
                component.render()  # Рендерим каждый компонент
        else:
            print("Window not created yet.")

    def add_component(self, component):
        """Добавление компонента в окно"""
        self.components.append(component)

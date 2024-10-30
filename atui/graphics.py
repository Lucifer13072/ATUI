import ctypes
import ctypes.wintypes
import sys

# Определяем структуру WNDCLASS
class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", ctypes.wintypes.UINT),
        ("lpfnWndProc", ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)),
        ("cbClsExtra", ctypes.wintypes.INT),
        ("cbWndExtra", ctypes.wintypes.INT),
        ("hInstance", ctypes.wintypes.HINSTANCE),
        ("hIcon", ctypes.wintypes.HICON),
        ("hCursor", ctypes.c_void_p),
        ("hbrBackground", ctypes.wintypes.HBRUSH),
        ("lpszMenuName", ctypes.wintypes.LPCWSTR),
        ("lpszClassName", ctypes.wintypes.LPCWSTR)
    ]

class Graphics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.hwnd = None  # Дескриптор окна

        # Создаем функцию обработчик сообщений
        self.wnd_proc_type = ctypes.WINFUNCTYPE(
            ctypes.c_long,
            ctypes.wintypes.HWND,
            ctypes.wintypes.UINT,
            ctypes.wintypes.WPARAM,
            ctypes.wintypes.LPARAM
        )(self.wnd_proc)

        # Создаем окно
        self.create_window()

    def create_window(self):
        # Регистрация класса окна
        wc = WNDCLASS()
        wc.style = 0
        wc.lpfnWndProc = self.wnd_proc_type  # Указываем обработчик оконных сообщений
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
        wc.hIcon = ctypes.windll.user32.LoadIconW(0, ctypes.wintypes.LPCWSTR(1))  # Замените 1 на ID иконки, если нужно
        wc.hCursor = ctypes.windll.user32.LoadCursorW(0, ctypes.wintypes.LPCWSTR(32512))  # ID стандартного курсора
        wc.hbrBackground = ctypes.windll.gdi32.GetStockObject(1)  # ID стандартного фона
        wc.lpszMenuName = None
        wc.lpszClassName = "MyWindowClass"

        # Регистрация класса
        ctypes.windll.user32.RegisterClassW(ctypes.byref(wc))

        # Создание окна
        self.hwnd = ctypes.windll.user32.CreateWindowExW(
            0,
            wc.lpszClassName,
            "Пустое Окно",
            0xCF0000,  # WS_OVERLAPPEDWINDOW
            100, 100,  # Позиция
            self.width, self.height,  # Размер
            0, 0,  # Родительское окно и меню
            0,  # Хэндл к хинду (в данном случае NULL)
            0,  # Приложение
            0  # Дополнительные параметры
        )

        # Отображение окна
        ctypes.windll.user32.ShowWindow(self.hwnd, 1)  # SW_SHOW
        ctypes.windll.user32.UpdateWindow(self.hwnd)

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == 0x0010:  # WM_CLOSE
            ctypes.windll.user32.DestroyWindow(hwnd)
            sys.exit(0)
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def show(self):
        # Главный цикл обработки событий
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

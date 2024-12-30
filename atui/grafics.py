import ctypes
from ctypes import wintypes

# Подключаем необходимые библиотеки
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)  # Для графических функций

# Определяем типы
WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

# Пользовательские типы
HCURSOR = wintypes.HANDLE  # Указатель на курсор
HICON = wintypes.HANDLE    # Указатель на иконку
HBRUSH = wintypes.HANDLE   # Указатель на кисть
HINSTANCE = wintypes.HANDLE  # Указатель на экземпляр приложения

# Определяем LRESULT вручную
LRESULT = ctypes.c_long if ctypes.sizeof(ctypes.c_void_p) == 4 else ctypes.c_int16

# Константы
WM_DESTROY = 0x0002
WS_OVERLAPPEDWINDOW = 0x00CF0000
CW_USEDEFAULT = 0x80000000

# Устанавливаем сигнатуры для используемых функций
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = LRESULT

user32.LoadCursorW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
user32.LoadCursorW.restype = HCURSOR

gdi32.GetStockObject.argtypes = [ctypes.c_int]
gdi32.GetStockObject.restype = HBRUSH

# Определение структуры WNDCLASS
class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ('style', ctypes.c_uint),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', wintypes.LPCWSTR),
        ('lpszClassName', wintypes.LPCWSTR),
    ]

# Функция обработки сообщений
def window_proc(hwnd, msg, wparam, lparam):
    if msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

# Преобразуем Python функцию в WNDPROC
WindowProc = WNDPROC(window_proc)

# Регистрация класса окна
wc = WNDCLASS()
wc.lpfnWndProc = WindowProc
wc.lpszClassName = "MyWindowClass"
wc.hInstance = kernel32.GetModuleHandleW(None)  # Получаем дескриптор текущего модуля
wc.hbrBackground = gdi32.GetStockObject(0)  # Белый фон

if not user32.RegisterClassW(ctypes.byref(wc)):
    raise ctypes.WinError(ctypes.get_last_error())

def generate(name, width, heigth):
    hwnd = user32.CreateWindowExW(
        0, wc.lpszClassName, name, WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, width, heigth,
        None, None, None, None
    )
    
    if not hwnd:
        raise ctypes.WinError(ctypes.get_last_error())

    # Показ окна
    user32.ShowWindow(hwnd, 1)
    user32.UpdateWindow(hwnd)

    # Главный цикл сообщений
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

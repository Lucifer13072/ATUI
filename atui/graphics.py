import ctypes
import ctypes.wintypes
# Имя класса окна
WNDCLASS_NAME = "MyWindowClass"
WM_SIZE = 0x0005
WM_DESTROY = 0x0002
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010

user32 = ctypes.windll.user32

def adjust_window_rect(hwnd, width, height):
    rect = ctypes.wintypes.RECT(0, 0, width, height)
    dw_style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE = -16
    user32.AdjustWindowRectEx(ctypes.byref(rect), dw_style, False, 0)
    return rect.right - rect.left, rect.bottom - rect.top

# Функция обратного вызова для обработки сообщений окна
def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == WM_DESTROY:  # WM_DESTROY
        ctypes.windll.user32.PostQuitMessage(0)  # Завершаем цикл сообщений
        return 0
    
    elif msg == WM_SIZE:
        # Получаем новый размер клиентской области
        width = lparam & 0xFFFF
        height = (lparam >> 16) & 0xFFFF
        print(f"Resized to: {width}x{height}")

        # Рассчитываем новый размер окна с учетом стиля
        win_width, win_height = adjust_window_rect(hwnd, width, height)
        
        # Используем MoveWindow для корректировки размера окна
        ctypes.windll.user32.MoveWindow(hwnd, None, None, win_width, win_height, True)
        
        # Перерисовываем содержимое окна, чтобы устранить черный фон
        ctypes.windll.user32.RedrawWindow(hwnd, None, None, 0x1)  # Флаг RDW_INVALIDATE
        ctypes.windll.user32.UpdateWindow(hwnd)  # Обновить окно
        return 0

    # Возвращаем сообщение по умолчанию
    return ctypes.windll.user32.DefWindowProcW(hwnd, msg, ctypes.wintypes.WPARAM(wparam), ctypes.wintypes.LPARAM(lparam))

# Определение структуры WNDCLASS для регистрации класса окна
class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", ctypes.wintypes.UINT),
        ("lpfnWndProc", ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)),
        ("cbClsExtra", ctypes.wintypes.INT),
        ("cbWndExtra", ctypes.wintypes.INT),
        ("hInstance", ctypes.wintypes.HINSTANCE),
        ("hIcon", ctypes.c_void_p),
        ("hCursor", ctypes.c_void_p),
        ("hbrBackground", ctypes.wintypes.HBRUSH),
        ("lpszMenuName", ctypes.wintypes.LPCWSTR),
        ("lpszClassName", ctypes.wintypes.LPCWSTR)
    ]

# Регистрация класса окна
def register_window_class():
    wndclass = WNDCLASS()
    wndclass.style = 0
    wndclass.lpfnWndProc = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)(wnd_proc)
    wndclass.cbClsExtra = 0
    wndclass.cbWndExtra = 0
    wndclass.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
    wndclass.hIcon = ctypes.c_void_p()
    wndclass.hCursor = ctypes.windll.user32.LoadCursorW(None, 32512)  # IDC_ARROW
    wndclass.hbrBackground = 0
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = WNDCLASS_NAME

    if ctypes.windll.user32.RegisterClassW(ctypes.byref(wndclass)) == 0:
        raise Exception("Failed to register window class")

    return wndclass

# Создание окна
def create_window(wndclass , w, h, title):
    hwnd = ctypes.windll.user32.CreateWindowExW(
        0,
        WNDCLASS_NAME,
        title,
        0xCF0000,  # WS_OVERLAPPEDWINDOW
        100, 100, w, h,
        None, None, ctypes.windll.kernel32.GetModuleHandleW(None), None
    )

    if hwnd == 0:
        error_code = ctypes.windll.kernel32.GetLastError()
        print(f"Failed to create window, error code: {error_code}")
        raise Exception("Failed to create window")

    ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW
    ctypes.windll.user32.UpdateWindow(hwnd)
    return hwnd

# Основная логика и цикл обработки сообщений
if __name__ == "__main__":
    try:
        wndclass = register_window_class()
        hwnd = create_window(wndclass, 800, 400, "Like")
        msg = ctypes.wintypes.MSG()
        while True:
            result = ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)
            if result == 0:  # WM_QUIT
                break  # Завершаем цикл
            
            # Обработка других сообщений
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

    except Exception as e:
        print("Error:", e)

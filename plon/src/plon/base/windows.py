import win32con
import win32gui
from cefpython3 import cefpython as cef
import win32api
import os
import math
import win32con


WindowUtils = cef.WindowUtils()

def close_window(window_handle, message, wparam, lparam):
    browser = cef.GetBrowserByWindowHandle(window_handle)
    if browser:
        browser.CloseBrowser(True)
    else:
        print('No Browser')
    # OFF: win32gui.DestroyWindow(window_handle)
    return win32gui.DefWindowProc(window_handle, message, wparam, lparam)


def exit_app(*_):
    win32gui.PostQuitMessage(0)
    return 0


def defocus(parentWindowHandle):
    print(User32.SetWindowLongW(
        parentWindowHandle, -20, 134217728))


def create_window(title, class_name, width, height, window_proc, icon, frameless=False):
    # Register window class
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = class_name
    wndclass.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32con.COLOR_WINDOW
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = window_proc
    atom_class = win32gui.RegisterClass(wndclass)
    assert(atom_class != 0)

    # Center window on screen.
    screenx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screeny = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    xpos = int(math.floor((screenx - width) / 2))
    ypos = int(math.floor((screeny - height) / 2))
    if xpos < 0:
        xpos = 0
    if ypos < 0:
        ypos = 0

    # Create window
    window_style = (win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN
                    | win32con.WS_VISIBLE)
    window_handle = win32gui.CreateWindow(class_name, title, window_style,
                                          xpos, ypos, width, height,
                                          0, 0, wndclass.hInstance, None)
    assert(window_handle != 0)

    # Window icon
    icon = os.path.abspath(icon)
    if not os.path.isfile(icon):
        icon = None
    if icon:
        # Load small and big icon.
        # WNDCLASSEX (along with hIconSm) is not supported by pywin32,
        # we need to use WM_SETICON message after window creation.
        # Ref:
        # 1. http://stackoverflow.com/questions/2234988
        # 2. http://blog.barthe.ph/2009/07/17/wmseticon/
        bigx = win32api.GetSystemMetrics(win32con.SM_CXICON)
        bigy = win32api.GetSystemMetrics(win32con.SM_CYICON)
        big_icon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON,
                                      bigx, bigy,
                                      win32con.LR_LOADFROMFILE)
        smallx = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        smally = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        small_icon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON,
                                        smallx, smally,
                                        win32con.LR_LOADFROMFILE)
        win32api.SendMessage(window_handle, win32con.WM_SETICON,
                             win32con.ICON_BIG, big_icon)
        win32api.SendMessage(window_handle, win32con.WM_SETICON,
                             win32con.ICON_SMALL, small_icon)

    if frameless:
        make_window_borderless(window_handle)

    return window_handle


window_proc = {
        win32con.WM_CLOSE: close_window,
        win32con.WM_DESTROY: exit_app,
        win32con.WM_SIZE: WindowUtils.OnSize,
        win32con.WM_SETFOCUS: WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: WindowUtils.OnEraseBackground
    }



import win32gui as wg
import win32api as wa
import win32con as wc

def make_window_borderless(hwnd):
    """
        Requires: pywin32
        https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32

        Based on: https://github.com/howardjohn/pyty/blob/master/src/window_api.py
    """
    def restore(hwnd):
        """
        Restores (unmaximizes) the window.
        Args:
            hwnd (int): The window handler.
        """
        wg.ShowWindow(hwnd, wc.SW_RESTORE)


    def maximize(hwnd):
        """
        Maximizes the window.
        Args:
            hwnd (int): The window handler.
        """
        wg.ShowWindow(hwnd, wc.SW_MAXIMIZE)

    def hwnd_for_title(title):
        def cb(hwnd, param):
            title = ''.join(char for char in wg.GetWindowText(hwnd) if ord(char) <= 126)
            d[title] = hwnd
        d = {}
        wg.EnumWindows(cb, title)
        if title in d:
            return d[title]
        else:
            return None

    # hwnd = hwnd_for_title(unit.window_name)
    style = wg.GetWindowLong(hwnd, wc.GWL_STYLE)
    style &= ~wc.WS_OVERLAPPEDWINDOW
    style |= wc.WS_POPUP
    wg.SetWindowLong(hwnd, wc.GWL_STYLE, style)

    rgb = wg.CreateSolidBrush(wa.RGB(0, 0, 0))
    GCLP_HBRBACKGROUND = -10
    wa.SetClassLong(hwnd, GCLP_HBRBACKGROUND, rgb)

    maximize(hwnd)
    restore(hwnd)

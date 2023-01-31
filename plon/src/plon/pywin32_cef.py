# Example of embedding CEF browser using PyWin32 library.
# Tested with pywin32 version 221 and CEF Python v57.0+.
#
# Usage:
#   python pywin32.py
#   python pywin32.py --multi-threaded
#
# By passing --multi-threaded arg CEF will run using multi threaded
# message loop which has best performance on Windows. However there
# is one issue with it on exit, see "Known issues" below. See also
# docs/Tutorial.md and the "Message loop" section.
#
# Known issues:
# - Crash on exit with multi threaded message loop (Issue #380)

from cefpython3 import cefpython as cef

import distutils.sysconfig
import math
import os
import platform
import sys

import win32api
import win32con
import win32gui

# Globals
WindowUtils = cef.WindowUtils()


import ctypes
User32 = ctypes.WinDLL('User32.dll')

from .base import conf, controller, windows


def update_conf(conf, **kw):
    for k, v in kw.items():
        setattr(conf, k,v)
    return conf


def main(**kw):
    command_line_args()
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    _conf = update_conf(conf, **kw)
    settings = {
        "multi_threaded_message_loop": _conf.multi_threaded_message_loop,
        **_conf.init_settings,
    }
    # https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
    cef.Initialize(settings=settings)
    frameless = getattr(_conf, 'frameless', False)
    window_handle = windows.create_window(**_conf.window, frameless=frameless)

    window_info = cef.WindowInfo()
    window_info.SetAsChild(window_handle)

    create_browser = controller.create_browser
    # defocus(window_info.parentWindowHandle)
    # defocus(window_handle)

    if _conf.multi_threaded_message_loop:
        # When using multi-threaded message loop, CEF's UI thread
        # is no more application's main thread. In such case browser
        # must be created using cef.PostTask function and CEF message
        # loop must not be run explicitilly.
        cef.PostTask(cef.TID_UI,
                     create_browser,
                     window_info,
                     {},
                     _conf.url)
        win32gui.PumpMessages()

    else:
        create_browser(window_info=window_info,
                       settings={},
                       url=_conf.url)
        cef.MessageLoop()

    cef.Shutdown()


def command_line_args():
    if "--multi-threaded" in sys.argv:
        sys.argv.remove("--multi-threaded")
        print("[pywin32.py] Message loop mode: CEF multi-threaded"
              " (best performance)")
        conf.multi_threaded_message_loop = True
    else:
        print("[pywin32.py] Message loop mode: CEF single-threaded")
    if len(sys.argv) > 1:
        print("ERROR: Invalid args passed."
              " For usage see top comments in pywin32.py.")
        sys.exit(1)


def check_versions():
    if platform.system() != "Windows":
        print("ERROR: This example is for Windows platform only")
        sys.exit(1)

    print("[pywin32.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[pywin32.py] Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))

    # PyWin32 version
    python_lib = distutils.sysconfig.get_python_lib(plat_specific=1)
    with open(os.path.join(python_lib, "pywin32.version.txt")) as fp:
        pywin32_version = fp.read().strip()
    print("[pywin32.py] pywin32 {ver}".format(ver=pywin32_version))

    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"



if __name__ == '__main__':
    main()

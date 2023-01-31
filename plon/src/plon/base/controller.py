from cefpython3 import cefpython as cef
from . import codes
import ctypes


def create_browser(window_info, settings, url):
    assert(cef.IsThread(cef.TID_UI))
    browser = cef.CreateBrowserSync(window_info=window_info,
                          settings=settings,
                          url=url)

    browser.SetClientHandler(FocusHandler(window_info))
    set_javascript_bindings(browser)
    return browser


def set_javascript_bindings(browser):
    '''
    Write and bind JS hook functionality.
    '''
    bindings = cef.JavascriptBindings(
            bindToFrames=True,
            bindToPopups=True
            )
    #bindings.SetProperty("python_property", "This property was set in Python")
    #bindings.SetProperty("cefpython_version", cef.GetVersion())
    # bindings.SetFunction("html_to_data_uri", html_to_data_uri)

    # external = External(browser)
    # bindings.SetObject("external", external)

    js_hooks = VOLJavascriptHook(browser)
    bindings.SetObject("VOL", js_hooks)
    browser.SetJavascriptBindings(bindings)
    # browser.ExecuteJavascript("setTimeout(function(){ console.log('timeout') }, 3000)")
    browser.ExecuteJavascript("console.log('Bound Javascript')")



class FocusHandler(object):
    def __init__(self, window_info):
        self.window_info = window_info
        # self.cef_widget.setFocusPolicy(Qt.NoFocus)

    def OnSetFocus(self, browser, **_):
        print('OnSetFocus')
        # defocus(self.window_info.parentWindowHandle)
        # browser.SetFocus(False)
        # browser.setFocusPolicy(Qt.NoFocus)
        # ctypes.windll.user32.keybd_event(0x41, 0, 0, 0)

    def OnGotFocus(self, browser, **_):
        print('OnGotFocus')
        # Temporary fix no. 1 for focus issues on Linux (Issue #284)
        # defocus(self.window_info.parentWindowHandle)
        # browser.SetFocus(False)


class VOLJavascriptHook(object):

    def __init__(self, browser):
        self.browser = browser

    def version(self):
        return 100

    def keyCall(self, key):
        code = codes.Codes[key.upper()]
        print('keyCall', key)
        ctypes.windll.user32.keybd_event(code, 0, 0, 0)

    def click(self, event):
        print('CLICK')

    # def test_multiple_callbacks(self, js_callback):
    #     """Test both javascript and python callbacks."""
    #     # js_print(self.browser, "Python", "test_multiple_callbacks", "Called from Javascript. Will call Javascript callback now.")

    #     def py_callback(msg_from_js):
    #         js_print(self.browser, "Python", "py_callback", msg_from_js)

    #     if hasattr(js_callback, 'Call'):
    #         js_callback.Call("String sent from Python", py_callback)
    #     else:
    #         print('Recv', js_callback)

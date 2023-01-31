from cefpython3 import cefpython as cef
from . import windows
from pathlib import Path


HERE = Path(__file__).parent
INIT_NAME = 'index.html'

RESOURCES = HERE.parent / 'cef100/bin'

url = HERE.parent / 'view' / INIT_NAME

multi_threaded_message_loop = False
memory_only = False
# frameless = True

window = dict(
    title="PyWin32 example",
    class_name="pywin32.example",
    width=800,
    height=600,
    window_proc=windows.window_proc,
    icon="resources/chromium.ico"
)


init_settings =dict(
    user_data_path='./userspace/data/',
    cache_path='./userspace/cache/',
    persist_user_preferences=int(memory_only),
    product_version="0.1",
    # remote_debugging_port=9876,
    # #https://learn.microsoft.com/en-gb/dotnet/api/skiasharp.skcolors?view=skiasharp-2.88
    background_color=0xFF111111,
    # resources_dir_path=str(RESOURCES),
    context_menu={
        # whether to enable mouse context menu
        "enabled": True,
        # show the "Back", "Forward" and "Reload" items. The "Reload" option calls
        # Browser.ReloadIgnoreCache.
        "navigation": False,
        # show the "Print..." item
        "print": False,
        # show the "View source" item
        "view_source": False,
        # show the "Open in external browser" and "Open frame in external browser"
        # options. On Linux the external browser is not focused when opening url.
        "external_browser": False,
        # show the "Developer Tools" option. See also
        # ApplicationSettings.remote_debugging_port.
        'devtools': True,
        }
)

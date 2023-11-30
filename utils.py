import numpy
import pywinauto
import pyautogui
import win32gui
import inspect
import time
import asyncio


LEAGUE_WINDOW_STR = "League of Legends (TM) Client"
RGB_BUSTER = (154, 155, 147)


def get_all_windows():
    windows = pywinauto.Desktop(backend="uia").windows()
    return windows
    return [w.window_text() for w in windows]


def get_windows_from_title(windows, substring):
    return [w for w in windows if substring in w.element_info.name]


def get_substring_from_lst(lst, substring):
    return [x for x in lst if substring in x][0]


def get_window_with_active(windows):
    return [w for w in windows if w.is_active()][0]


def does_window_exist(window_title):
    def callback(hwnd, extra):
        titles.append(win32gui.GetWindowText(hwnd))

    titles = []
    win32gui.EnumWindows(callback, None)

    return any(window_title in title for title in titles)


async def await_buster(timeout=20, startup_timeout=20, keepwindowon=False):
    all_windows = get_all_windows()

    league_window = None
    while startup_timeout > 0 and not league_window:
        if i := get_windows_from_title(all_windows, LEAGUE_WINDOW_STR):
            league_window = i[0]

        await asyncio.sleep(1)
        startup_timeout -= 1

    if not league_window:
        yield "LEAGUE WINDOW COULD NOT BE LOCATED"
        return

    yield "FOUND WINDOW, STARTING TRACKING"

    while 1:
        all_windows = get_all_windows()
        last = get_window_with_active(all_windows)
        last_mouse = pyautogui.position()

        if not win32gui.GetWindowText(league_window.element_info.handle):
            yield "GAME ENDED"
            return

        if league_window.is_minimized():
            league_window.restore()
            await asyncio.sleep(0.5)

        league_window.set_focus()
        scr = league_window.capture_as_image()

        # count pixels on screen
        cnt = 0
        for x in range(scr.width):
            for y in range(scr.height):
                cnt += 1 if scr.getpixel((x, y)) == RGB_BUSTER else 0

        print(cnt)
        if cnt > 10:
            yield f"POSSIBLE AFK MESSAGE DETECTED WITH {cnt} PIXELS OF COLOUR {RGB_BUSTER}"

        if last != league_window:
            if not keepwindowon:
                league_window.minimize()
            last.set_focus()
            pyautogui.moveTo(*last_mouse)

        await asyncio.sleep(timeout)


def loop():
    if await_buster(keepwindowon=True):
        # disc bot or smth
        pass
    else:
        # game ended
        pass


if __name__ == "__main__":
    loop()

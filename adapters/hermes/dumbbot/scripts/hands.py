"""DumbBot hands, by noxeldev (MIT). Slow, safe mouse and keyboard for Windows.

The brain is the AI agent that calls this file. These are only the hands.

LOOK
  hands.py doctor                          check this PC is ready (packages, screen, admin) and paste it when asking for help
  hands.py windows                         visible windows (title, process)
  hands.py active                          the focused window
  hands.py shot [file.png] [--window "title"] [--scale 0.5]
                                           screenshot; --window crops to that window and prints its
                                           rect, so you can use click X Y --rel (coordinates inside it)
  hands.py ui-list --window "title"        buttons, fields and menus by NAME (needs pywinauto)
  hands.py ui-read ["name"] --window "t"   read the text of a field (default: the main edit area)

ACT (every action needs --expect "window title"; --focus brings it to the front first)
  hands.py focus "title part"              bring a window to the front
  hands.py click X Y --expect "t" [--focus] [--rel] [--double]
  hands.py ui-click "name" --expect "t" [--focus]   press a control by name (no mouse, no coordinates)
  hands.py paste "text" --expect "t" [--focus]      paste through the clipboard (your clipboard is restored)
  hands.py key ctrl+l --expect "t" [--focus]
  hands.py save-dialog "C:/dir/file.ext"   wait for a Windows Save As window and save there
  hands.py wait-title "title part" [sec]   wait until a window title appears

click, paste, key and ui-click also print "changed": true/false = did the window look different
afterwards. It is a hint, not proof: still look at a screenshot.

Safety: move the mouse to a screen corner to stop everything (PyAutoGUI fail-safe).
Guard: input is refused unless the focused window matches --expect. Never into the programs in
NEVER_TYPE_IN. Browsers are refused too (use a browser tool for web pages) unless the window is a
native dialog such as Save As, or DUMBBOT_ALLOW_BROWSER=1. Daily cap: DUMBBOT_MAX_ACTIONS (default 400).
Never deletes. Never types passwords. Never sends messages on its own.
"""
import argparse, ctypes, hashlib, json, os, random, sys, time
from ctypes import wintypes
from datetime import date
from pathlib import Path

try:
    import pyautogui
    import pyperclip
except ImportError as e:
    print(json.dumps({"ok": False, "error": f"missing package: {e.name}",
                      "fix": "ask the user, then run: pip install pyautogui pyperclip"}))
    raise SystemExit(2)

try:  # make window rectangles and mouse coordinates agree on high-DPI screens
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15

NEVER_TYPE_IN = {"cmd.exe", "powershell.exe", "pwsh.exe", "regedit.exe", "taskmgr.exe", "mmc.exe"}
BROWSERS = {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe", "vivaldi.exe", "arc.exe"}
STATE = Path(os.environ.get("DUMBBOT_STATE", Path.home() / ".dumbbot"))
STATE.mkdir(parents=True, exist_ok=True)
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def say(**kw):
    print(json.dumps(kw, ensure_ascii=False))


def title_of(hwnd):
    n = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(hwnd, buf, n + 1)
    return buf.value


def class_of(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, 256)
    return buf.value


def rect_of(hwnd):
    r = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(r))
    return r.left, r.top, r.right - r.left, r.bottom - r.top


def process_of(hwnd):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    kernel32.OpenProcess.restype = wintypes.HANDLE
    h = kernel32.OpenProcess(0x1000, False, pid.value)
    if not h:
        return ""
    try:
        size = wintypes.DWORD(520)
        buf = ctypes.create_unicode_buffer(520)
        if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            return os.path.basename(buf.value).lower()
        return ""
    finally:
        kernel32.CloseHandle(h)


def active():
    h = user32.GetForegroundWindow()
    return h, title_of(h), process_of(h)


def visible_windows():
    out = []
    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def cb(h, _):
        if user32.IsWindowVisible(h) and title_of(h).strip():
            out.append((h, title_of(h), process_of(h)))
        return True

    user32.EnumWindows(EnumProc(cb), 0)
    return out


def find_window(part):
    for h, t, p in visible_windows():
        if part.lower() in t.lower():
            return h, t, p
    return None


def budget():
    f = STATE / "actions.json"
    today = str(date.today())
    d = {"day": today, "n": 0}
    try:
        d = json.loads(f.read_text())
        if d.get("day") != today:
            d = {"day": today, "n": 0}
    except Exception:
        pass
    cap = int(os.environ.get("DUMBBOT_MAX_ACTIONS", "400"))
    if d["n"] >= cap:
        raise SystemExit(say(ok=False, error=f"daily cap {cap} reached"))
    d["n"] += 1
    f.write_text(json.dumps(d))


def guard(expect, refocus=False):
    """Refuse to act unless the focused window is the expected one.
    With refocus, first bring the expected window to the front (the agent's own app often takes
    the foreground between calls), then check again. The check itself is never skipped."""
    if refocus and expect:
        focus(expect)
    h, t, p = active()
    if p in NEVER_TYPE_IN:
        raise SystemExit(say(ok=False, error=f"blocked process {p}"))
    if not expect:
        raise SystemExit(say(ok=False, error="--expect is required: name the window that must be in front"))
    if expect.lower() not in t.lower():
        raise SystemExit(say(ok=False, error="wrong window in front", front=t, expected=expect))
    if p in BROWSERS and class_of(h) != "#32770" and os.environ.get("DUMBBOT_ALLOW_BROWSER") != "1":
        raise SystemExit(say(ok=False, error="browser page: use a browser tool for web pages "
                                             "(native dialogs such as Save As are allowed)"))
    budget()
    return h


def pause(a=0.3, b=0.9):
    time.sleep(random.uniform(a, b))


def slow_move(x, y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.6, 1.2), tween=pyautogui.easeInOutQuad)


def bring_front(h):
    """Foreground a window without tapping Alt (an Alt tap puts apps like Notepad in menu mode)."""
    cur = user32.GetForegroundWindow()
    me = kernel32.GetCurrentThreadId()
    fg = user32.GetWindowThreadProcessId(cur, None)
    attached = bool(fg and fg != me and user32.AttachThreadInput(me, fg, True))
    try:
        user32.ShowWindow(h, 9)
        user32.BringWindowToTop(h)
        user32.SetForegroundWindow(h)
        if user32.GetForegroundWindow() != h:
            user32.SwitchToThisWindow(h, True)  # fallback, no Alt tap
    finally:
        if attached:
            user32.AttachThreadInput(me, fg, False)


def focus(part, tries=3):
    for _ in range(tries):
        for h, t, p in visible_windows():
            if part.lower() in t.lower() and p not in NEVER_TYPE_IN:
                bring_front(h)
                pause(0.4, 0.8)
                if part.lower() in active()[1].lower():
                    return True
        pause(0.5, 1.0)
    return False


def fingerprint(h):
    """Small hash of what a window looks like, to tell if an action changed anything."""
    try:
        x, y, w, hh = rect_of(h)
        img = pyautogui.screenshot(region=(max(x, 0), max(y, 0), max(w, 1), max(hh, 1))).convert("L").resize((96, 54))
        return hashlib.md5(img.tobytes()).hexdigest()
    except Exception:
        return None


def paste(text):
    """Paste through the clipboard and put the user's previous text clipboard back."""
    try:
        old = pyperclip.paste()
    except Exception:
        old = None
    pyperclip.copy(text)
    pause()
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    if old is not None:
        try:
            pyperclip.copy(old)
        except Exception:
            pass


def wait_title(part, sec=60):
    t0 = time.time()
    while time.time() - t0 < sec:
        if part.lower() in active()[1].lower():
            return True
        time.sleep(0.3)
    return False


def finish(h, before):
    time.sleep(0.7)
    after = fingerprint(h)
    say(ok=True, changed=(before is not None and after is not None and before != after))


# ---------- Windows UI Automation (optional: pip install pywinauto) ----------

def uia_window(part):
    try:
        from pywinauto import Desktop
    except ImportError:
        raise SystemExit(say(ok=False, error="missing package: pywinauto",
                             fix="ask the user, then run: pip install pywinauto"))
    found = find_window(part)
    if not found:
        raise SystemExit(say(ok=False, error=f"no window with title containing {part!r}"))
    return Desktop(backend="uia").window(handle=found[0])


def uia_controls(win, limit=150):
    out = []
    try:
        for c in win.descendants():
            try:
                info = c.element_info
                name = (info.name or "").strip()
                ctype = info.control_type
                if not name and ctype not in ("Edit", "Document"):
                    continue
                if not info.visible:
                    continue
                r = info.rectangle
                out.append((c, {"name": name, "type": ctype, "id": info.automation_id,
                                "enabled": bool(info.enabled),
                                "rect": [r.left, r.top, r.right - r.left, r.bottom - r.top]}))
                if len(out) >= limit:
                    break
            except Exception:
                continue
    except Exception as e:
        raise SystemExit(say(ok=False, error=f"UI Automation failed: {e}"))
    return out


def uia_find(win, name):
    items = uia_controls(win, 400)
    exact = [c for c, i in items if i["name"].lower() == name.lower()]
    part = [c for c, i in items if name.lower() in i["name"].lower()]
    pick = exact or part
    if not pick:
        raise SystemExit(say(ok=False, error=f"no control named {name!r}"))
    return pick[0]


def uia_text(c):
    for getter in ("get_value", "window_text"):
        try:
            v = getattr(c, getter)()
            if v:
                return v
        except Exception:
            pass
    try:
        return c.iface_value.CurrentValue
    except Exception:
        return ""


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("windows")
    sub.add_parser("active")
    s = sub.add_parser("shot"); s.add_argument("file", nargs="?"); s.add_argument("--window"); s.add_argument("--scale", type=float, default=1.0)
    s = sub.add_parser("focus"); s.add_argument("title")
    s = sub.add_parser("click"); s.add_argument("x", type=int); s.add_argument("y", type=int)
    s.add_argument("--expect"); s.add_argument("--focus", action="store_true"); s.add_argument("--double", action="store_true"); s.add_argument("--rel", action="store_true")
    s = sub.add_parser("paste"); s.add_argument("text"); s.add_argument("--expect"); s.add_argument("--focus", action="store_true")
    s = sub.add_parser("key"); s.add_argument("keys"); s.add_argument("--expect"); s.add_argument("--focus", action="store_true")
    s = sub.add_parser("save-dialog"); s.add_argument("path"); s.add_argument("--wait", type=int, default=120)
    s = sub.add_parser("wait-title"); s.add_argument("title"); s.add_argument("sec", nargs="?", type=int, default=60)
    s = sub.add_parser("ui-list"); s.add_argument("--window", required=True)
    s = sub.add_parser("ui-read"); s.add_argument("name", nargs="?"); s.add_argument("--window", required=True)
    s = sub.add_parser("ui-click"); s.add_argument("name"); s.add_argument("--expect"); s.add_argument("--focus", action="store_true")
    a = ap.parse_args()

    if a.cmd == "doctor":
        try:
            import pywinauto  # noqa: F401
            uia = True
        except ImportError:
            uia = False
        w, h = pyautogui.size()
        h_front, t, p = active()
        say(ok=True, packages={"pyautogui": True, "pyperclip": True, "pywinauto": uia},
            screen=[w, h], monitors=user32.GetSystemMetrics(80),
            run_as_admin=bool(ctypes.windll.shell32.IsUserAnAdmin()),
            front={"title": t, "process": p}, python=sys.version.split()[0],
            tips=[t2 for t2, bad in [
                ("install pywinauto for the ui-* commands: pip install pywinauto", not uia),
                ("more than one monitor: keep the target window on the main one", user32.GetSystemMetrics(80) > 1),
                ("nothing is in front (screen locked or asleep?)", not t and not p)] if bad])
    elif a.cmd == "windows":
        say(windows=[{"title": t, "process": p} for _, t, p in visible_windows()])
    elif a.cmd == "active":
        _, t, p = active(); say(title=t, process=p)
    elif a.cmd == "shot":
        f = a.file or str(STATE / f"shot_{int(time.time())}.png")
        info = {}
        if a.window:
            found = find_window(a.window)
            if not found:
                raise SystemExit(say(ok=False, error=f"no window with title containing {a.window!r}"))
            x, y, w, h = rect_of(found[0])
            x, y = max(x, 0), max(y, 0)
            img = pyautogui.screenshot(region=(x, y, w, h))
            info = {"window": found[1], "rect": [x, y, w, h]}
        else:
            img = pyautogui.screenshot()
        if a.scale and a.scale != 1.0:
            img = img.resize((max(1, int(img.width * a.scale)), max(1, int(img.height * a.scale))))
            info["scale"] = a.scale
            info["note"] = "multiply coordinates by 1/scale before using click"
        img.save(f)
        say(ok=True, file=f, size=[img.width, img.height], **info)
    elif a.cmd == "focus":
        say(ok=focus(a.title), front=active()[1])
    elif a.cmd == "click":
        h = guard(a.expect, a.focus)
        x, y = a.x, a.y
        if a.rel:
            wx, wy, _, _ = rect_of(h)
            x, y = wx + x, wy + y
        before = fingerprint(h)
        slow_move(x, y); pause(0.2, 0.5)
        (pyautogui.doubleClick if a.double else pyautogui.click)()
        finish(h, before)
    elif a.cmd == "paste":
        h = guard(a.expect, a.focus); before = fingerprint(h)
        paste(a.text); finish(h, before)
    elif a.cmd == "key":
        h = guard(a.expect, a.focus); before = fingerprint(h)
        pyautogui.hotkey(*a.keys.split("+")); finish(h, before)
    elif a.cmd == "ui-list":
        win = uia_window(a.window)
        say(ok=True, controls=[i for _, i in uia_controls(win)])
    elif a.cmd == "ui-read":
        win = uia_window(a.window)
        if a.name:
            c = uia_find(win, a.name)
        else:
            cs = [c for c, i in uia_controls(win, 400) if i["type"] in ("Edit", "Document")]
            if not cs:
                raise SystemExit(say(ok=False, error="no text area found"))
            c = cs[0]
        say(ok=True, text=uia_text(c)[:2000])
    elif a.cmd == "ui-click":
        h = guard(a.expect, a.focus); before = fingerprint(h)
        win = uia_window(a.expect)
        c = uia_find(win, a.name)
        try:
            c.invoke()                      # no mouse involved
        except Exception:
            slow_move(*[int(v) for v in (c.rectangle().mid_point().x, c.rectangle().mid_point().y)])
            pause(0.2, 0.5); pyautogui.click()
        finish(h, before)
    elif a.cmd == "save-dialog":
        t0 = time.time()
        while time.time() - t0 < a.wait:
            if active()[1].lower() in ("save as", "guardar como"):
                pause(0.8, 1.4); pyautogui.hotkey("ctrl", "a"); pause(0.3, 0.5)
                paste(a.path); pause(0.6, 1.0)
                if active()[1].lower() in ("save as", "guardar como"):
                    pyautogui.press("enter"); say(ok=True, saved=a.path)
                else:
                    say(ok=False, error="dialog changed, nothing sent")
                return
            time.sleep(0.3)
        say(ok=False, error="no Save As window appeared")
    elif a.cmd == "wait-title":
        say(ok=wait_title(a.title, a.sec))


if __name__ == "__main__":
    main()

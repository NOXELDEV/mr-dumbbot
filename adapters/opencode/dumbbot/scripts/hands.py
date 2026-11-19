"""DumbBot hands, by noxeldev (MIT). Slow, safe mouse and keyboard for Windows.

The brain is the AI agent that calls this file. These are only the hands.

  python hands.py windows                       list visible windows (title, process)
  python hands.py active                        show the focused window
  python hands.py shot [file.png]               screenshot
  python hands.py focus "title part"            bring a window to the front
  python hands.py click X Y --expect "title" [--focus]  slow click, only if that window is in front
                                                (--focus brings it to the front first, same command)
  python hands.py paste "text" --expect "title" paste text (clipboard), only if guard passes
  python hands.py key ctrl+l --expect "title"   press keys, only if guard passes
  python hands.py save-dialog "C:\\path\\file"  wait for a Save As window, save there
  python hands.py wait-title "title part" [sec] wait until a window title appears

Safety: move the mouse to a screen corner to stop everything (PyAutoGUI fail-safe).
Guard: input is refused unless the focused window matches --expect, and never goes to
a process in NEVER_TYPE_IN (edit it). Daily cap on actions via DUMBBOT_MAX_ACTIONS (default 400).
Never deletes. Never types passwords. Never sends messages on its own.
"""
import argparse, ctypes, json, os, random, sys, time
from ctypes import wintypes
from datetime import date
from pathlib import Path

try:
    import pyautogui
    import pyperclip  # noqa: F401
except ImportError as e:
    print(json.dumps({"ok": False, "error": f"missing package: {e.name}",
                      "fix": "ask the user, then run: pip install pyautogui pyperclip"}))
    raise SystemExit(2)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15

NEVER_TYPE_IN = {"cmd.exe", "powershell.exe", "pwsh.exe", "regedit.exe", "taskmgr.exe", "mmc.exe"}
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
    _, t, p = active()
    if p in NEVER_TYPE_IN:
        raise SystemExit(say(ok=False, error=f"blocked process {p}"))
    if not expect:
        raise SystemExit(say(ok=False, error="--expect is required: name the window that must be in front"))
    if expect.lower() not in t.lower():
        raise SystemExit(say(ok=False, error="wrong window in front", front=t, expected=expect))
    budget()


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


def paste(text):
    import pyperclip
    pyperclip.copy(text)
    pause()
    pyautogui.hotkey("ctrl", "v")


def wait_title(part, sec=60):
    t0 = time.time()
    while time.time() - t0 < sec:
        if part.lower() in active()[1].lower():
            return True
        time.sleep(0.3)
    return False


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("windows")
    sub.add_parser("active")
    s = sub.add_parser("shot"); s.add_argument("file", nargs="?")
    s = sub.add_parser("focus"); s.add_argument("title")
    s = sub.add_parser("click"); s.add_argument("x", type=int); s.add_argument("y", type=int); s.add_argument("--expect"); s.add_argument("--focus", action="store_true"); s.add_argument("--double", action="store_true")
    s = sub.add_parser("paste"); s.add_argument("text"); s.add_argument("--expect"); s.add_argument("--focus", action="store_true")
    s = sub.add_parser("key"); s.add_argument("keys"); s.add_argument("--expect"); s.add_argument("--focus", action="store_true")
    s = sub.add_parser("save-dialog"); s.add_argument("path"); s.add_argument("--wait", type=int, default=120)
    s = sub.add_parser("wait-title"); s.add_argument("title"); s.add_argument("sec", nargs="?", type=int, default=60)
    a = ap.parse_args()

    if a.cmd == "windows":
        say(windows=[{"title": t, "process": p} for _, t, p in visible_windows()])
    elif a.cmd == "active":
        _, t, p = active(); say(title=t, process=p)
    elif a.cmd == "shot":
        f = a.file or str(STATE / f"shot_{int(time.time())}.png")
        pyautogui.screenshot(f); say(ok=True, file=f)
    elif a.cmd == "focus":
        say(ok=focus(a.title), front=active()[1])
    elif a.cmd == "click":
        guard(a.expect, a.focus); slow_move(a.x, a.y); pause(0.2, 0.5)
        (pyautogui.doubleClick if a.double else pyautogui.click)(); say(ok=True)
    elif a.cmd == "paste":
        guard(a.expect, a.focus); paste(a.text); say(ok=True)
    elif a.cmd == "key":
        guard(a.expect, a.focus); pyautogui.hotkey(*a.keys.split("+")); say(ok=True)
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

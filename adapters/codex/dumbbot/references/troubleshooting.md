# Troubleshooting

Run `hands.py doctor` first. It checks packages, screen, monitors and admin mode. (It shows the title of the front window; remove it before sharing if it is private.)

| Symptom | Likely cause | What to do |
|---|---|---|
| `missing package: ...` | Python packages not installed | Ask the user, then `pip install pyautogui pyperclip` (and `pywinauto`). |
| `wrong window in front` | Another app took the focus (your own app, a notification, a pop-up) | Add `--focus`. Ask the user to silence notifications and not touch the PC. |
| `ok: true` but nothing happened | `ok` only means keys were sent | Confirm with `shot` or `ui-read`. Look for a pop-up, a menu left open or the wrong text field. |
| Text went to the menu letters (F, E, V...) in an app | The Alt key was tapped | Fixed in `focus` (no Alt). Press Escape once and retry. |
| `no Save As window appeared` | The download did not start, or the dialog is named differently | Check the page first. Look at a screenshot. Do not click Download again before checking. |
| It clicks the wrong place | Window moved, scaling, several monitors | Prefer `ui-click` by name. Use `shot --window` and `click --rel`. Keep the app on the main monitor. |
| Nothing responds, no error | Screen locked or asleep, or an admin/UAC window is in front | Wake the PC. Ask the user to handle the prompt. DumbBot cannot control admin windows unless it also runs as admin. |
| `browser page: use a browser tool...` | `hands.py` does not act on web pages | Use the browser tool. Native dialogs (Save As) are allowed. |
| `daily cap reached` | Safety limit hit | Ask the user. Raise `DUMBBOT_MAX_ACTIONS` only if they agree. |
| An app reopens the old document (Notepad does) | The app restores its last session | Check the title and contents before select-all or delete. Never save over a file you did not create. |
| The mouse is out of control | -- | Move the mouse to a screen corner. Everything stops. |

If it still fails after 2 tries: stop, tell the user what you see and what you tried. Do not keep clicking.

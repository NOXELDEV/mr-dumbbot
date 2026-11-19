# Safety and responsible use

## Enforced by the code (`hands.py`)
1. **Emergency stop:** moving the mouse to any screen corner halts everything (PyAutoGUI fail-safe). Always warn the user before the mouse starts moving.
2. **Window guard:** click, paste and key require `--expect "<window title>"` and are refused if another window is in front.
3. **Blocklist:** never types into cmd, PowerShell, regedit, Task Manager, mmc (`NEVER_TYPE_IN`). Browser pages are refused too (use a browser tool); native dialogs like Save As are allowed. Set `DUMBBOT_ALLOW_BROWSER=1` only if the user explicitly wants that.
4. **Daily action cap:** `DUMBBOT_MAX_ACTIONS` (default 400) so a loop cannot run away. The counter is kept in `DUMBBOT_STATE` (default `~/.dumbbot`).
5. **Never deletes.** Nothing in the hands deletes files.

## Rules for the agent
- Three tries, then ask for help.
- Never message people and never publish: that is the user's decision.
- Never press Send/Submit unless the user said so for that job.
- Never type passwords. The user signs in themself.
- Back up a file before editing it.

## Responsible use
- Use it on **your own PC and your own accounts**, for your own work. The user is responsible for respecting the terms of every site and app they automate; some limit automated access, and an account can be limited or closed.
- Never use it to bypass CAPTCHAs or other bot checks, send spam or mass messages, create many accounts, cheat in tests or games, or access anything the user is not allowed to use.
- Stay slow and within the caps. DumbBot imitates a patient person; it is not for flooding a service.
- If a task looks like it breaks a site's rules or harms someone, stop and tell the user.

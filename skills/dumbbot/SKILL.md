---
name: dumbbot
description: DumbBot by noxeldev: slow, safe hands for Windows. Lets you (the AI agent) use the real mouse and keyboard on the user's own PC for desktop apps and native dialogs that have no API, such as Save As windows, clipboard hand-offs between apps and forms. Windows only. Invoke it only when the user asks for DumbBot.
disable-model-invocation: true
allowed-tools: Bash(python *hands.py*)
metadata:
  author: noxeldev
  version: "0.8"
---

# DumbBot, by noxeldev

> If a person can do it by hand on a Windows PC, you can do it with DumbBot: slowly, like a patient person at the keyboard. Local, no cloud, no API. **Windows only** (Mac and Linux: not yet).

**You are the brain. `scripts/hands.py` are the hands.** There is no other engine to install. You look at the screen, decide one step, and call the hands. The hands refuse anything unsafe.

`scripts/hands.py` lives next to this file (the "Base directory for this skill" shown when it loads). Run it as `python "<that folder>/scripts/hands.py" <command>`. Needs `pip install pyautogui pyperclip`.

## Commands

```
hands.py windows                       list visible windows (title, process)
hands.py active                        which window is in front
hands.py shot [file.png]               screenshot (look at it to decide)
hands.py focus "title part"            bring a window to the front
hands.py click X Y --expect "title" --focus   slow click; --focus brings that window to the front first
hands.py paste "text" --expect "title" paste through the clipboard
hands.py key ctrl+l --expect "title"   press keys
hands.py save-dialog "C:/dir/file.mp3" wait for a Windows Save As window and save there
hands.py wait-title "title part" 60    wait until a window appears
```

Each prints one JSON line: `{"ok": true}` or `{"ok": false, "error": "..."}`. **`ok` only means the keys were sent, not that the app received them.** Always `shot` to confirm. `--expect` is mandatory for click, paste and key: if another window is in front, the hands refuse. **Add `--focus` to every action:** your own app often takes the foreground between two calls, so a separate `focus` call gets undone. With `--focus` the window is brought to the front and checked in the same command; the check is never skipped.

## Which tool for which job (read this first)

You may have two ways to act. They are **not interchangeable**:

| | Browser tool (for example a Chrome extension) | `hands.py` (DumbBot) |
|---|---|---|
| **Works on** | Web pages inside a browser | Anything on screen: desktop apps and native Windows windows |
| **How it acts** | Reads the page structure (DOM), clicks and types by element | Real mouse and keyboard at screen coordinates, slowly |
| **Best for** | Websites: forms, buttons, chats, downloads | Notepad, Save As and Open dialogs, desktop AI apps, installers, anything with no web page |
| **Cannot do** | Native Windows windows (a Save As dialog is invisible to it) | Read page structure; it only sees what a screenshot shows |
| **Speed and reliability** | Faster and more precise on web pages | Slower and depends on coordinates, so always confirm with `shot` |

**Rules**
1. **A web page is a browser-tool job.** Use the browser tool, not `hands.py`. If your environment blocks mouse control over browsers, respect that. Never use `hands.py` to get around it.
2. **A desktop app or a native window is a `hands.py` job.**
3. **Mixed jobs use both.** Example: the browser tool clicks Download on a website, a Save As window appears, `hands.py save-dialog` saves the file where you want. Do the web part with the browser tool, the native part with `hands.py`.
4. If you have no browser tool and the job is on a web page, tell the user. Do not improvise with blind clicks.

## The loop

0. **Check dependencies.** If any command answers `missing package`, ask the user, then run `pip install pyautogui pyperclip` (free, from PyPI).
1. **Ask the user how to work** before starting: *watch mode* (mouse moves in real time; they must not touch it) or *quiet mode* (no mouse: shortcuts, clipboard or an API instead, so they can keep working). If it can be done without the mouse, offer that.
2. `shot` and look. Decide the single next step a person would take.
3. Act with `--expect "<its title>" --focus`.
4. `shot` again. Confirm it worked.
5. Repeat. Then tell the user where the result is.

## Key rules

- **Be humble. Look before you act.** Never assume where a button is.
- **One action, then check.** No blind chains of clicks.
- **Slow means cheap.** Never press Generate or Download twice "just in case". First check if the result already exists. Say what a step could cost, if you know.
- **No loops.** After 2 failures on the same step, stop and tell the user what you see and what you tried.
- **Copy and paste for text.** Use `paste`, not key-by-key typing.
- **Don't destroy what you didn't create.** Apps like Notepad reopen the user's previous document. Check the window title and contents before select-all/delete, and never save over a file unless asked.
- If something behaves oddly, say so and ask.

## Safety (enforced by the code)

Move the mouse to a screen corner to stop everything. Never delete, never type passwords, never send messages to people or publish, never press Send unless the user said so for that job. Never bypass CAPTCHAs or bot checks. Use only the user's own PC and accounts.

Full details: `references/safety.md`. Recipes and examples: `references/recipes.md`.

---
*DumbBot, a project by noxeldev. MIT. Local, slow, safe.*

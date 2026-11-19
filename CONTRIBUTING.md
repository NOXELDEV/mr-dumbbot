# Contributing to Mr. DumbBot / Cómo ayudar

DumbBot is small on purpose: a skill plus one file (`skills/dumbbot/scripts/hands.py`). It is easy to read, so it is easy to improve.
DumbBot es pequeño a propósito: un skill y un archivo (`hands.py`). Es fácil de leer, así que es fácil de mejorar.

## New here? / ¿Eres nuevo?
- Try the Notepad test from the README and tell us how it went (open a **Feedback** issue). Your confusion is useful: it shows what the docs are missing.
- Prueba el test del Bloc de notas del README y cuéntanos cómo te fue (issue de **Feedback**). Tu confusión sirve: muestra qué falta en la documentación.
- Improving the wording of `SKILL.md` or `references/troubleshooting.md` is a great first contribution.

## Experienced? Ideas that would help most / Ideas con más valor
- Test on other Windows setups: another language, high DPI, several monitors, antivirus on. Report what breaks.
- Make `ui-click` and `ui-list` more reliable on apps beyond Notepad (Explorer, Office, Electron apps).
- Recipes people can reuse (keep them in `recipes/`).
- Safer defaults and better refusals (see `references/safety.md`).
- macOS and Linux versions of `hands.py`.
- A small automated smoke test.

## Rules that do not change / Reglas que no cambian
1. **Safety lives in the code.** Don't weaken the window guard (`--expect`), the blocklist, the daily cap, the browser refusal or the mouse-to-corner stop.
2. **No stealth.** Nothing that hides automation or gets around bot checks, CAPTCHAs, or platform restrictions.
3. **Never deletes, never types passwords, never messages people or publishes.**
4. **Be honest in the docs.** Say what you tested and what you did not.

## How to send a change / Cómo enviar un cambio
1. Fork, make a branch, change **`skills/dumbbot/`** (the source). The folders in `adapters/` and the zips are generated; don't edit them by hand.
2. Run `python skills/dumbbot/scripts/hands.py doctor` and try your change on a harmless window such as Notepad.
3. Open a pull request and say what you tested.

MIT licensed. By contributing you agree your work is released under the same license.

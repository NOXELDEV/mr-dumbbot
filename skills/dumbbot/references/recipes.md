# Recipes and examples

A recipe is just the list of steps a person would do, written down so it can be repeated. Do the job once in real time, then save the steps (a short `.md` or a small script that calls the same `hands.py` commands) in a `recipes/` folder of your own.

## Examples to adapt (not limits)
- Move an image or file from one app to another through the clipboard.
- Relay text between AI apps: paste a question, wait, copy only the answer, save it.
- Save downloads into the right folder through the Save As dialog (`save-dialog`).
- Fill the same form from a spreadsheet, without pressing Send unless allowed.
- Download recurring reports from portals the user is signed in to.
- Run a list of jobs (one per line) within the daily cap.

## Web pages
For pages inside a browser, use the browser tools your agent already has (for example a browser extension) and use `hands.py` only for native apps and native dialogs such as Save As. Some agents restrict mouse control over browsers; respect that and never work around it. See the table in `SKILL.md`: "Which tool for which job".

## Making a recipe with the user
1. Ask them to do the task once by hand and describe it.
2. Write each step as one command (`focus`, `click`, `paste`, `key`, `save-dialog`).
3. Put `--expect` on every click, paste and key.
4. Add a check (`shot`) after each step that matters.
5. Test it with the mouse-to-corner stop in mind.

## What to tell the user
- **Before:** "DumbBot is going to use your mouse for about N minutes. Please don't touch it. Move the mouse to a corner to stop it."
- **After:** say where the output is, in plain words.
- **On error:** explain simply. If the error says the result **was** already produced, do not run it again (it could spend credits twice).

# Mr. DumbBot

**By noxeldev.** Slow, safe hands for AI agents on **Windows**. The agent is the brain; `hands.py` moves the real mouse and keyboard, locally. No cloud, no API.
**Por noxeldev.** Manos lentas y seguras para agentes de IA en **Windows**. El agente es el cerebro; `hands.py` mueve el mouse y el teclado reales, en local. Sin nube y sin API.

> Windows only for now. / Solo Windows por ahora.

## What it does / Qué hace

- A toolkit to build your own slow-hands automations. / Una caja de herramientas para crear tus propias automatizaciones lentas.
- Handles native Windows dialogs (Save As) that browser automation can't touch. / Maneja diálogos de Windows (Guardar como) que la automatización del navegador no alcanza.
- Hands text and files between apps through the clipboard. / Pasa texto y archivos entre apps por el portapapeles.
- Fills repeated forms, never pressing Send on its own. / Llena formularios repetidos sin pulsar Enviar solo.

## Why / Por qué

- **Dumb on purpose:** it follows exact steps; the thinking comes from you or your agent. / **Tonto a propósito:** sigue pasos exactos; el pensamiento viene de ti o de tu agente.
- **Safe in code:** corner-stop, window guard on every click/paste/key, blocklist, daily action cap, never deletes. / **Seguro en el código:** parada en la esquina, guardia de ventana en cada clic/pegado/tecla, lista de bloqueo, tope diario, nunca borra.
- **Local and private:** nothing leaves your PC; you sign in to your own accounts. / **Local y privado:** nada sale de tu PC; tú inicias sesión en tus cuentas.

## For beginners / Para principiantes

**EN.** Your AI assistant can already do a lot by itself: read your files, talk to apps that have a connector, and work on web pages. Use that first. It is faster.
But some things have no connector and no web page: a Windows "Save As" window, a desktop program, a repetitive click-here-then-there job. That is where DumbBot helps: it lets the AI use your mouse and keyboard **slowly, one visible step at a time**, so you can watch, understand and stop it (mouse to a screen corner).

**ES.** Tu asistente de IA ya hace mucho solo: lee tus archivos, usa apps con conector y trabaja en páginas web. Usa eso primero, es más rápido.
Pero hay cosas sin conector ni página web: una ventana "Guardar como" de Windows, un programa de escritorio, una tarea repetitiva de clics. Ahí ayuda DumbBot: deja que la IA use tu mouse y teclado **despacio, un paso visible a la vez**, para que puedas mirar, entender y pararlo (mouse a una esquina de la pantalla).

| Situation / Situación | Use / Usa |
|---|---|
| Has a connector, API or command / Hay conector, API o comando | The native way / Lo nativo |
| It is a web page / Es una página web | The browser tool / La herramienta de navegador |
| Native Windows window (Save As, installer) / Ventana nativa de Windows | **DumbBot** |
| Desktop app with no integration / Programa de escritorio sin integración | **DumbBot** |
| Repetitive job you want to watch / Tarea repetitiva que quieres ver | **DumbBot** |
| The platform or you said no to something / Tú o la plataforma dijeron que no | Neither. Never a way around a restriction / Ninguna. Nunca para esquivar una restricción |

DumbBot is slow on purpose so you can follow it. It is **not** for hiding automation or avoiding bot checks.
DumbBot es lento a propósito para que lo puedas seguir. **No** sirve para ocultar automatización ni para saltar controles anti-bot.

The `dumbbot-guide` skill lets your AI notice these situations by itself and suggest DumbBot (it only advises and asks first). The `dumbbot` skill does the work and only starts when you type `/dumbbot`.
El skill `dumbbot-guide` deja que tu IA note estas situaciones sola y te sugiera DumbBot (solo aconseja y pregunta antes). El skill `dumbbot` hace el trabajo y solo arranca cuando escribes `/dumbbot`.

## Before you run it / Antes de ejecutarlo

**EN.** Most "it doesn't work" reports come from touching the PC while DumbBot works. So:
1. **Leave the PC alone** while it works: no mouse **and no keyboard**, even in quiet mode.
2. **Silence pop-ups:** chat apps, notifications, update prompts (turn on Do Not Disturb).
3. **Keep the screen awake:** no lock, no sleep. Don't minimize the target app.
4. **Save your other work** and close what you don't need. One monitor is best.
5. Windows **admin windows and security prompts (UAC) can't be controlled**: you handle those.
6. **To stop it:** move the mouse to a corner of the screen.

**ES.** La mayoría de los "no funciona" vienen de tocar la PC mientras DumbBot trabaja. Por eso:
1. **Deja la PC en paz** mientras trabaja: ni mouse **ni teclado**, aunque sea modo silencioso.
2. **Silencia lo que pueda saltar:** chats, notificaciones, avisos de actualización (activa No molestar).
3. **Mantén la pantalla despierta:** sin bloqueo ni suspensión. No minimices la app que usa.
4. **Guarda tu otro trabajo** y cierra lo que no necesites. Mejor con un solo monitor.
5. Las **ventanas de administrador y los avisos de seguridad (UAC) no se pueden controlar**: los atiendes tú.
6. **Para pararlo:** mueve el mouse a una esquina de la pantalla.

## If it doesn't work / Si no funciona

Run `python skills/dumbbot/scripts/hands.py doctor` and read `skills/dumbbot/references/troubleshooting.md` (a table of symptoms and fixes). If you open an issue, paste the `doctor` output (remove the window title if it is private).
Ejecuta `python skills/dumbbot/scripts/hands.py doctor` y lee `skills/dumbbot/references/troubleshooting.md` (tabla de síntomas y soluciones). Si abres un issue, pega el resultado de `doctor` (quita el título de la ventana si es privado).

## Install / Instalar

Needs / Necesita: Windows 10/11, Python 3.10+, `pip install pyautogui pyperclip`.

**Claude Code (plugin):**
```
/plugin marketplace add noxeldev/mr-dumbbot
/plugin install dumbbot@mr-dumbbot
```
Then use it with `/dumbbot`. It is **manual-only**: Claude will not start moving your mouse on its own.

**Any agent (Claude Code, OpenCode, Codex, Hermes):** run `install.ps1`. It copies the skill to every agent it finds on your PC.

**claude.ai:** upload `dumbbot-skill.zip` as a skill.

## Files / Archivos

- `skills/dumbbot/`: the skill that does the work (`SKILL.md`, `references/`, `scripts/hands.py`). / el skill que hace el trabajo.
- `skills/dumbbot-guide/`: the guide that tells the AI when to suggest DumbBot. / la guía que dice a la IA cuándo sugerir DumbBot.
- `adapters/`: the same skill with the right header for Claude Code, OpenCode, Codex and Hermes. / el mismo skill con el encabezado de cada agente.
- `tests/trigger-prompts.md`: phrases to check when it should and should not be used. / frases para comprobar cuándo usarlo y cuándo no.

## Responsible use / Uso responsable

Use it on your own PC and accounts. You are responsible for following the terms of each site you automate. Do not use it to bypass CAPTCHAs, send spam, create fake accounts or cheat.
Úsalo en tu propia PC y cuentas. Tú eres responsable de cumplir los términos de cada sitio que automatices. No lo uses para saltar CAPTCHAs, hacer spam, crear cuentas falsas ni hacer trampa.

## Support / Apoyo

If DumbBot helps you, a small donation is welcome and keeps it going. Thank you!
Si DumbBot te ayuda, una donación pequeña se agradece y lo mantiene vivo. ¡Gracias!

**Donate / Donar:** [ko-fi.com/noxeldev](https://ko-fi.com/noxeldev)

## License / Licencia

MIT. See `LICENSE`. / MIT. Mira `LICENSE`.

© noxeldev

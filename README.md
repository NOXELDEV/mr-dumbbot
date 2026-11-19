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

- `skills/dumbbot/`: the skill (`SKILL.md`, `references/`, `scripts/hands.py`). / el skill.
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

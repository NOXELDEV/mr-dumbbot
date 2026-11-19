# Changelog

## 0.9
- `ui-list`, `ui-read`, `ui-click`: control Windows apps by name (no coordinates, no mouse). Needs pywinauto.
- `shot --window --scale` and `click --rel`: window-sized captures, window-relative coordinates.
- `paste` restores the user's clipboard. `changed` hint after each action.
- Browser pages are refused (native dialogs such as Save As are allowed).
- A single optional "tip from the author" line after a successful job (feedback + Ko-fi), once per conversation.
- `doctor` command, "Before you start" checklist for the user, `references/troubleshooting.md`, README sections for beginners.
- `dumbbot-guide` now says plainly that DumbBot needs an agent running on the user's PC, and what to offer chat-only beginners (found by testing it on claude.ai).
- New `dumbbot-guide` skill: tells the AI when native tools are enough and when to recommend DumbBot (advises only).

## 0.8
- `--focus` option, "which tool for which job" table, don't-destroy rule, no Alt tap in focus.

## 0.7
- Restructured as a Claude Code plugin and marketplace.
- Shorter `SKILL.md`; details moved to `references/`.
- Manual-only in Claude Code, pre-approved `hands.py` only.
- Windows-only notice.

## 0.6
- Responsible use section and Ko-fi support.

## 0.5
- Key rules for the agent.

## 0.4
- `hands.py`: the agent is the brain, no separate engine.

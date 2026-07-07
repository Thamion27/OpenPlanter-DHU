# CIB-8 Windows Runtime Guardrails

## Purpose

These guardrails control how local agent models operate inside the Chairman's Windows OpenPlanter-DHU workspace.

## Operating Environment

- OS: Windows
- Shell: PowerShell
- Repo path: E:\DHU\OpenPlanter-DHU
- Local runtime: OpenPlanter CLI
- Local models: Ollama models such as ornith:35b and dhu-ornith-builder

## Command Rules

Agents must use Windows PowerShell commands only.

Allowed examples:
- Get-ChildItem
- Get-Content
- Select-String
- Select-Object
- Test-Path
- New-Item
- Set-Content
- Add-Content
- python
- py

Forbidden Unix-style commands:
- ls
- head
- grep
- cat
- pwd
- python3
- rm
- cp
- mv
- chmod
- Unix pipe assumptions

## File Modification Rule

Agents must not modify files unless the Chairman explicitly authorizes file creation or editing.

Forbidden unless authorized:
- write_file
- apply_patch
- edit_file
- delete_file
- shell commands that create, overwrite, move, or delete files

## Preferred Inspection Order

1. Use read_file for known files.
2. Use list_files for broad repo inspection.
3. Use search_files for code search.
4. Use PowerShell only when tool inspection is insufficient.
5. Never use shell as the first choice when read_file can answer.

## Protected Paths

Never write to or commit:
- .venv/
- .env
- .env.*
- .openplanter/
- secrets
- API keys
- private credentials

## CIB-8 Safety Boundary

CIB-8 must collect lawful signals only.

Agents must not assist with:
- hacking
- credential theft
- illegal surveillance
- private-message interception
- doxxing
- stalking
- coercive HUMINT
- unauthorized scanning
- bypassing access controls

## Evidence Rule

Every investigative claim must include:

- Claim
- Evidence
- Source
- Confidence
- Limitation
- Recommended next action

## Human Authority Rule

The Chairman is the hands and final authority.

Agents may recommend changes, but only the Chairman executes repo changes unless he explicitly says: "Execute it."

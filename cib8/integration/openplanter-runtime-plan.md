# CIB-8 OpenPlanter Runtime Integration Plan

## Purpose
CIB-8 is the command doctrine. OpenPlanter is the execution chassis. Ornith 35B is the local scaffold/code engineer candidate. The Chairman remains the human operator and final authority.

## Integration Principle
Do not rewrite OpenPlanter first. First connect CIB-8 through prompts, templates, and controlled runtime instructions. Code changes come only after doctrine works in dry runs.

## Existing OpenPlanter Capabilities To Use
- Headless task execution
- Local Ollama provider
- Recursive mode
- Tool calling
- File reading
- Search tools
- Subtask delegation
- Session persistence
- Acceptance criteria
- Test suite

## CIB-8 Runtime Flow
User Mission -> CIB-8 Mission Brief -> Layer Selection -> OpenPlanter Layer Tasks -> Evidence Return Packets -> Evidence Fusion -> Red-Team QC -> Final Dossier -> Human-approved Hindsight Skills

## First Integration Target
Create a CIB-8 mission prompt that can be passed into OpenPlanter headless mode.

## Later Files Likely Involved
- agent/prompts.py
- agent/engine.py
- agent/tool_defs.py
- agent/tools.py
- tests/
- cib8/

## First Tests To Create Later
- test_cib8_guardrails.py
- test_cib8_mission_brief.py
- test_cib8_layer_selection.py
- test_cib8_evidence_packet.py
- test_cib8_no_unauthorized_write.py

## Safety Requirements
CIB-8 must not assist with hacking, credential theft, illegal surveillance, stalking, doxxing, private-message interception, coercive HUMINT, unauthorized scanning, or bypassing access controls.

## Human Authority Rule
No autonomous repo changes. Agents may recommend changes. The Chairman executes changes. GPT-5.5 Thinking provides doctrine, QC, and architecture. Ornith 35B assists locally with scaffolding and code planning.

## Next Approved Step
Run a CIB-8 mission-planning dry run using OpenPlanter and Ornith 35B. The dry run must read the CIB-8 doctrine and guardrail files, and must not modify files.

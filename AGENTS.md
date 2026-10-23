# AGENTS.md

This file is the central index for project documentation and the standing instructions for agents working in this repository. Its scope is the entire repository.

## Project Documents

Keep this index current as the project grows.

### Project Foundations

- [Project manifest](docs/MANIFEST.md) - the purpose and values of Wiki Greblje.
- [Development workflow](docs/README.txt) - the project's development sequence and documentation notes.

### Current State and Planning

- [Current project status](docs/STATUS_2026-10-23.md) - the latest consolidated implementation and production status.
- [Historical status, 14 October 2026](docs/STATUS_2026-10-14.md) - the state before the advanced-search work.
- [TODO](docs/TODO.md) - completed work, pending verification, backlog, and deploy-ready changes.
- [Roadmap](docs/Roadmap.md) - planned capabilities and confirmed implementation status.
- [Sprint history](docs/SPRINTS.md) - sprint goals, results, and later recorded work.
- [Ideas](docs/IDEAS.md) - future ideas and open planning questions.
- [Changelog](docs/CHANGELOG.md) - recorded product changes and historical additions.

### Decisions and Operations

- [Decision log](docs/DECISIONS.md) - accepted project and product decisions with their rationale.
- [Deployment guide](docs/DEPLOYMENT.md) - environment details, safe deployment steps, and operational lessons.

### Design and UI

- [Design principles](docs/DESIGN-PRINCIPLES.md) - heritage representation and public moderation principles.
- [Design notes](docs/DESIGN.md) - applied visual and implementation guidance.
- [Design system](docs/DESIGN_SYSTEM.md) - shared components and their use across the product.
- [UI guidelines](docs/UI_GUIDELINES.md) - interface philosophy, visual rules, and interaction guidance.
- [WGDS component overview](docs/WGDS.md) - the working Heritage Person Panel specification.
- [WG-PERSON-001 specification](docs/WGDS/WG-PERSON-001.md) - the component specification and its verification status.

### Visual References

- [Sprint 1 desktop reference](docs/screenshots/Sprint1/s1-d.png)
- [Sprint 1 mobile reference](docs/screenshots/Sprint1/s1-m.png)
- [Sprint 1 tablet reference](docs/screenshots/Sprint1/s1-t.png)

### AI Agent Context

- [AI agent project context](AgentsDocs/AI_AGENT_PROJECT_CONTEXT.md) - consolidated project goals, completed work, current status, constraints, and source map for future agents.
- [Conversation-derived topic index](AgentsDocs/Topics/README.md) - thematic operational knowledge recovered from the shared project conversation.
- [MapTiler and coordinate handling](AgentsDocs/Topics/MAPTILER_AND_COORDINATES.md) - map migration history, localization fixes, source paths, and recurring diagnostics.
- [Remote access and server topology](AgentsDocs/Topics/REMOTE_ACCESS_AND_SERVER.md) - WireGuard, SSH, server roles, and safe access notes.
- [Deployment and environment history](AgentsDocs/Topics/DEPLOYMENT_AND_ENVIRONMENT.md) - production deploy sequence, environment recovery, backups, and commit history.
- [Roles, permissions, and classification](AgentsDocs/Topics/ROLES_PERMISSIONS_AND_CLASSIFICATION.md) - editor/expert role model and role-aware classification behavior.
- [Cemetery proposals and moderation](AgentsDocs/Topics/CEMETERY_PROPOSALS_AND_MODERATION.md) - public proposal workflow, approval rules, public filtering, and deployment status.
- [Photos and gallery behavior](AgentsDocs/Topics/PHOTOS_AND_GALLERY.md) - photo permissions, moderation, public visibility, and gallery incident history.
- [Grave entry, persons, and OCR](AgentsDocs/Topics/GRAVE_ENTRY_PERSON_AND_OCR.md) - entry workflow, empty-person regression, validation, and OCR status.

### Agent Change Reports

- [Branch-specific change reports](AgentsDocs/Changes/) - handoff records that preserve task context between agents and accounts.

## Always Do

- Keep the project document links in this file up to date whenever a document is added, moved, renamed, or retired.
- For every prompt that results in project work, create a small Markdown report in `AgentsDocs/Changes/<current-git-branch>/`. Name it `<five-digit-index>_<small-description>.md`, starting with `00001`. Determine the next index from the reports already in that branch's folder and increment the highest index by one. Every report must include:
  - the prompt execution date and time, including the time zone;
  - the original prompt verbatim;
  - a description of the task;
  - the changes made for the prompt;
  - the reasons for implementation decisions; and
  - links to related earlier or follow-up reports, or an explicit statement that there are none.

## Never Do

- Never do what you are not asked to do.

# 00001 - Create AGENTS.md and Project Documentation Index

- Prompt execution datetime: `2026-10-21T15:35:03+02:00`
- Git branch: `main`

## Original Prompt

```text
Create me AGENTS.md file in project root. In here we will link up all of the documents related to the project and we have to keep updating it as project grows.
Please add `Always Do` section in there and add following points:
- At the AgentsDocs/Changes/<current git branch> always generate a small report .md file with naming of <index relative to the current folder, starting at 00001>_<small description>.md. In there We must have datetime of prompt execution, original given prompt, changes done in the prompt, description of the task, reasons why something is done some way and rest of the relative reports. This will be used to pass on coding tasks from account to account, so context of project can be preserved from agent to agent. Each next doc must be increment of the last index relative to the folder in it

Please add `Never Do` section and add point:
- Never do what you are not asked to do
```

## Task Description

Create a repository-wide `AGENTS.md` that acts as the maintained index of project documentation and defines the requested rules for agent change reports and task scope.

## Changes Made

- Created the root `AGENTS.md`.
- Linked every current project document under `docs/`, including the three Sprint 1 visual references.
- Added the `Always Do` section with the document-index maintenance rule and the branch-specific, sequential report convention.
- Added the `Never Do` section with the requested scope restriction.
- Created `AgentsDocs/Changes/main/` and this first report using index `00001`.

## Decisions and Reasons

- The document links are grouped by purpose so future agents can find the relevant context quickly.
- Both WGDS documents are linked because they have similar structures but different status notes; neither was assumed to replace the other.
- Report indexes use five zero-padded digits to match the requested `00001` starting format and preserve filename sorting.
- The active branch was read from `.git/HEAD` because the Git executable is not available on this environment's `PATH`.
- Related reports are represented as Markdown links so task context can be followed across handoffs.

## Related Reports

None. This is the first report in `AgentsDocs/Changes/main/`.

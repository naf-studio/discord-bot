# Contributing to Discord Bot

Thank you for your interest in contributing to the discord-bot project at NAF Studio. This document outlines our engineering standards, contribution workflow, and architectural conventions.

---

## 1. Branching Strategy & Workflow

This project adheres to a streamlined Trunk-based Development model:

- `main`: The stable production branch. All modifications targeting `main` must be submitted via a Pull Request and pass all continuous integration checks.
- Working branches should be branched directly from `main` using structured naming:
  - `feat/<short-description>`: New commands, listeners, or capabilities.
  - `fix/<short-description>`: Bug fixes, exception handling, or operational resolutions.
  - `refactor/<short-description>`: Code restructuring or performance optimizations without functional changes.
  - `chore/<short-description>`: Dependency updates, build configuration, or CI maintenance.
  - `docs/<short-description>`: Technical documentation and guide revisions.

---

## 2. Commit Standards

### 2.1. Conventional Commits

All commit messages must adhere to the Conventional Commits specification:

```text
<type>(<scope>): <short description>
```

- Allowed Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- Optional Scope: Component or module name (e.g., `admin`, `events`, `server`, `config`).
- Description: Concise imperative sentence in lowercase without trailing punctuation.

### 2.2. Atomic Commits

- Each commit must address a single logical concern.
- Never mix formatting changes, dependency bumps, and business logic modifications within the same commit.
- Every commit must leave the codebase in a functional, compilable state that can be reverted safely without collateral breakage.

---

## 3. Coding Standards

### 3.1. Verification Pipeline

- Environment Manager: `uv`.
- Linter and Formatter: `ruff` (configured via `pyproject.toml`).
- Static Type Checker: `ty`.
- Prior to submitting code or creating commits, all verification commands must pass:

  ```bash
  uv run ruff check .
  uv run ruff format --check .
  ty check
  ```

### 3.2. Comment Hygiene and Docstrings

- Write clean, self-documenting code. Avoid trivial line-by-line comments (e.g., `# loop through items`, `# check if valid`).
- PEP 257 Docstrings is required for all modules, classes, and public functions or methods:
  - Summarize the purpose in the first line using imperative mood.
  - Detail parameters, return types, and exceptions when non-obvious.
  - Maintain a concise, technical engineering tone.

---

## 4. Architecture & Clean Code Principles

- Source code resides inside `src/discord_bot/`, ensuring strict separation from configuration assets and preventing namespace collisions.
- Group related command handlers and event listeners inside dedicated `commands.Cog` modules within `src/discord_bot/cogs/`.
- Never invoke unconditional global command syncing (`tree.sync()`) on startup. Use the administrative `/sync` command to register commands safely.
- All environment variables and runtime secrets are parsed through `Settings` (`pydantic-settings`) in `src/discord_bot/config.py`.
- Unhandled interaction errors are intercepted by `tree.error` to provide helpful user feedback while preventing interaction timeouts.

---

## 5. Pull Request Process

1. Ensure your feature branch is rebased on top of the latest `main`.
2. Verify all local checks pass: `uv run ruff check .`, `uv run ruff format --check .`, and `ty check`.
3. Open a Pull Request on GitHub. The pre-configured template will be populated automatically.
4. Provide a clear summary of your changes and reference relevant issues (e.g., `Closes #12`).
5. Merging requires passing CI workflows and maintainer approval.

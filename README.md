# NAF Studio - Discord Bot

Community automation Discord bot powered by `discord.py`, architected with modular cogs, and optimized for both modern local toolchains (`uv`, `ruff`, `ty`) and universal deployment on standard hosting panels (`python` + `pip`).

---

## 1. Architectural Overview & System Design

```text
discord-bot/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── pull_request_template.md
├── config/
│   └── messages/
├── discord_bot/
│   ├── cogs/
│   ├── __init__.py
│   ├── __main__.py
│   ├── bot.py
│   ├── config.py
│   └── main.py
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── main.py                <-- Universal entrypoint runner
├── pyproject.toml         <-- Modern packaging, scripts & tool configuration
├── requirements.txt       <-- Synchronized production dependencies for pip hosts
├── uv.lock
└── README.md
```

### Engineering Decisions & Standards

- Eliminates intermediate `src/` nesting while retaining strict package encapsulation. This guarantees zero-friction imports (`from discord_bot.main import main`) on constrained host panels that execute `python main.py` without package installation steps.
- Ships with a locked, pre-compiled `requirements.txt` exported from `pyproject.toml`, ensuring out-of-the-box compatibility with hosting panels that strictly rely on `pip install -r requirements.txt`.
- Discord imposes a hard quota of 200 global application command sync requests per day. Global syncing on boot is disabled by default (`SYNC_COMMANDS_ON_STARTUP=false`). Operators synchronize on-demand using `/sync [guild|global]`.
- Global interaction error handling maps unhandled exceptions, missing permissions, and cooldowns to structured ephemeral feedback without hanging interaction lifecycles.
- Dual-output logging multiplexes formatted records to console `stdout` and a size-capped `RotatingFileHandler` in `logs/bot.log`.
- Strictly validated against `ty` (Astral's high-performance Python type checker) and typed with complete type annotations.

---

## 2. Deployment on Standard Hosting Panels

### 1. File Upload & Setup

Upload or clone the repository to your host server. The panel will automatically recognize `requirements.txt` and `main.py`.

### 2. Dependency Installation

Most panels install dependencies automatically upon startup. If manual installation is required:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory (or use your host panel's Environment Variables manager).

### 4. Startup Command

Set the panel startup command to:

```bash
python main.py
```

---

## 3. Local Development with `uv`

### Prerequisites

- Python `>= 3.12`
- [uv](https://docs.astral.sh/uv/)
- [ty](https://github.com/astral-sh)

### Dependency Synchronization

```bash
uv sync --all-extras
```

### Running Locally

```bash
uv run discord-bot
uv run python -m discord_bot
uv run python main.py
```

### Regenerating `requirements.txt`

When adding or updating dependencies in `pyproject.toml`, synchronize `requirements.txt` for hosting compatibility:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

---

## 4. Code Quality, Linting & Type Checking

Ensure all verification pipelines pass locally before pushing changes:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
```

---

## 5. Contributing

Contributions must follow the standards outlined in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 6. License

This project is licensed under the [MIT License](LICENSE). Copyright &copy; 2024 [naipret](https://github.com/naipret).

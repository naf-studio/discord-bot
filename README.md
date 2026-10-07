# NAF Studio - Discord Bot

Community automation Discord bot powered by `discord.py`, architected with modular cogs, and built with modern Python tooling.

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
├── src/
│   └── discord_bot/
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── main.py
├── pyproject.toml
└── README.md
```

### Engineering Standards

- Conforms to standard PyPA `src-layout`, preventing top-level namespace collision while providing native entrypoint packaging via `[project.scripts]`.
- Discord imposes a hard quota of 200 global application command sync requests per day. Global syncing on boot is disabled by default (`SYNC_COMMANDS_ON_STARTUP=false`). Operators synchronize on-demand using `/sync [guild|global]`.
- Global interaction error handling maps unhandled exceptions, missing permissions, and cooldowns to structured ephemeral feedback without hanging interaction lifecycles.
- Dual-output logging multiplexes formatted records to console `stdout` and a size-capped `RotatingFileHandler` in `logs/bot.log`.
- Strictly validated against `ty` (Astral's high-performance Python type checker) and typed with complete type annotations.

---

## 2. Getting Started

### Prerequisites

- Python `>= 3.12`
- [uv](https://docs.astral.sh/uv/)
- [ty](https://github.com/astral-sh)

### Dependency Installation

```bash
uv sync
```

### Environment Configuration

Copy the template file to create your local `.env`:

```bash
cp .env.example .env
```

Configure parameters in `.env`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `BOT_TOKEN` | Discord Bot Authentication Token | `required` |
| `PERMISSIONS` | OAuth2 permissions integer for bot invite link | `8` |
| `OWNER_ID` | Discord user ID of the primary administrator | `0` |
| `SYNC_COMMANDS_ON_STARTUP` | Auto-sync application commands on startup | `false` |
| `LOG_LEVEL` | Application logging level (`DEBUG`, `INFO`, `WARNING`) | `INFO` |
| `DISCORD_INVITE_LINK` | Public Discord invite URL | `https://discord.nafmc.xyz/` |
| `JOIN_CHANNEL_ID` | Audit channel ID for member join logs | `0` |
| `LEAVE_CHANNEL_ID` | Audit channel ID for member departure logs | `0` |
| `BOOST_CHANNEL_ID` | Audit channel ID for boost announcements | `0` |

### Running the Bot

Launch through any of the supported execution vectors:

```bash
uv run discord-bot

uv run python -m discord_bot

uv run python main.py
```

---

## 3. Code Quality, Linting & Type Checking

Ensure all verification pipelines pass locally:

```bash
uv run ruff check .

uv run ruff format --check .

ty check
```

---

## 4. Contributing

Contributions must follow the standards outlined in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 5. License

This project is licensed under the [MIT License](LICENSE). Copyright &copy; 2024 [naipret](https://github.com/naipret).

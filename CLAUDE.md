# Project Rules

## Context Documents

Read these before making architectural decisions or starting non-trivial work:

- `docs/ARCHITECTURE.md` — system design, data flow, agent pipeline, tech stack decisions
- `docs/STATUS.md` — current task backlog, in-progress work, and what's done
- `docs/DECISIONS.md` — architectural decision log (ADRs)

## Project Summary

Autonomous swing trading bot for precious metals (NYSE, NYSE Arca, NASDAQ). Runs on a FastAPI server with `arq`-based background jobs. Uses PydanticAI agents over OpenRouter LLMs. Trades via Alpaca. Data from Finnhub, TwelveData, Reddit. Stores state in PostgreSQL. Controlled via Telegram bot. Visualised via local Metabase.

## General

- Do not modify unrelated files
- Respect existing project structure and patterns
- Avoid overengineering MVP features
- Before any architectural decision, check `docs/DECISIONS.md` to avoid re-litigating settled questions
- Record new architectural decisions as ADRs in `docs/DECISIONS.md`

## Python Style (applies to *.py files)

- Follow the Google Python Style Guide
- Use "double quotes" for strings
- Prefer explicit imports
- Keep functions short and composable
- Avoid magic numbers — put constants in `src/config/constants.py`
- Prefer small, surgical changes over large rewrites

## Testing (applies to tests/*.py)

- Use pytest for testing, NEVER use unittest or import from it
- Write tests for new functionality
- Write the shortest, most minimalist tests possible that cover core functionality
- Use coverage.py to track test coverage
- Use pytest-cov to report test coverage
- Use pytest-mock to mock dependencies

## PydanticAI Agent Conventions (applies to src/agents/**/*.py)

Each agent module must define, in order: a typed `Deps` dataclass, a `Result(BaseModel)`, the `Agent` instance, tool functions, and an async `run_<name>` entrypoint.

- `Deps` must be a typed dataclass — never `dict` or `Any`
- All result models must include `confidence: float` (0.0–1.0)
- Use `@agent.tool` when the tool needs `RunContext`; use `@agent.tool_plain` when it does not
- Every tool must have a docstring — it becomes the tool description sent to the LLM
- Dynamic system prompts that depend on runtime state use `@agent.system_prompt(dynamic=True)`
- Raise `ModelRetry` inside a tool to signal the LLM should retry with corrected input
- Multi-agent: subagents are called via tools on the supervisor agent; each subagent result is serialised to JSON before being passed up
- The supervisor is the only agent that may call the trader agent

## Trading Guardrails (applies to src/agents/trader.py, src/services/portfolio/)

- Maximum loss per trade: `position_size = (total_capital * 0.025) / abs(entry_price - stop_loss_price)` — never derive position size without this check
- Every trade record requires: `ticker`, `entry_price`, `stop_loss`, `take_profit`, `expiry_date`, `thesis` (non-empty string), `position_size`
- Reject (raise, never silently default) if any required field is missing
- Expiry-triggered sales must write a learnings entry to `trade_journal` (thesis held? explanation, prices, duration) — do not skip even if the LLM call fails
- Guardrail order: check liquidity → size position → validate fields → execute → record

## Research Cache TTLs (applies to src/services/research/)

Per-metric TTLs — do not cache "no cache" metrics, do not extend TTLs without an ADR:

| Metric | TTL |
|---|---|
| `market_cap`, `category`, `jurisdiction_risk`, `aisc`, `institutional_interest`, `upcoming_catalysts` | 30 days |
| `short_term_returns` (3d/7d/14d) | 1 day |
| `volume_spikes`, `volatility`, `metal_correlation`, `news_sentiment`, `social_sentiment`, `analyst_sentiment`, `insider_trades`, `option_flows` | no cache |

Cache key format: `"{ticker}:{metric}"`. Always store `fetched_at` alongside the value and validate expiry in code — do not rely on DB-level TTL alone. Never cache an error or empty response.

## Skills

- `db-migrate` — Alembic migration workflow (generate, apply, rollback, inspect). See `.claude/skills/db-migrate/SKILL.md`.

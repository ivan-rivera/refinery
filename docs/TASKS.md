# Status

This document outlines status of tasks that need to be completed.

## Tasks

- [ ] Set up environment config (pydantic `Settings` class)
- [ ] Set up PostgreSQL with SQLAlchemy + Alembic migrations
- [ ] Create DB schema: `holdings`, `trades`, `learnings`, `research_cache`
- [ ] Set up `arq` with Redis for background job management
- [ ] Set up FastAPI app skeleton with health check endpoint
- [ ] Connect to Alpaca API (auth, client wrapper)
- [ ] Find appropriate data sources (human only)
- [ ] Implement `get_positions()` — fetch current holdings from Alpaca
- [ ] Implement `place_order()` — the `trade()` tool; enforce 2.5% max loss rule internally, set stop-loss/take-profit before submitting
- [ ] Implement `close_position()` — used for expiry and stop-loss exits
- [ ] `get_holdings()` — join Alpaca positions with metadata from `holdings` table (thesis, expiry, entry price)
- [ ] `record_trade()` — write new trade to `holdings` with thesis + expiry
- [ ] `check_expiries()` — identify positions past expiry date, trigger close + learning
- [ ] `record_learning()` — summarise outcome of a closed trade, write to `trades` + `learnings`
- [ ] `get_liquidity()` — determine available capital for new positions
- [ ] Finnhub client — news, insider trades, analyst sentiment
- [ ] TwelveData client — price history, technicals, volume
- [ ] Alpaca market data client — supplementary OHLCV
- [ ] Reddit scraper — target relevant subs (e.g. r/wallstreetbets, r/investing, r/Gold)
- [ ] Blog/news scraper — configurable list of sources
- [ ] `get_candidates()` — aggregate tickers from screeners, Reddit, news, blogs
- [ ] `quick_filter()` — eliminate based on hard rules (volume, market cap floor, exchange, sector)
- [ ] `rank_candidates()` — lightweight scoring to prioritise research queue
- [ ] `ResearchCoordinator` — orchestrates subagents, assembles final report
- [ ] `SentimentAgent` — news + social + analyst sentiment scoring
- [ ] `TechnicalAgent` — volume spikes, volatility, short-term returns, metal correlation
- [ ] `CatalystAgent` — upcoming events, insider trades, option flows (stub for now)
- [ ] `FundamentalsAgent` — market cap, category, jurisdiction risk, AISC (cache: 30d)
- [ ] `SupervisorAgent` — receives consolidated report + learnings context, produces trade recommendation with suggested expiry
- [ ] Implement research caching — skip cached fields, only refresh no-cache metrics on repeat tickers
- [ ] `TraderAgent` — receives supervisor recommendation, calls `trade()` tool, records thesis
- [ ] Wire up guardrails in `trade()` tool — 2.5% rule, exchange whitelist, position size caps
- [ ] Implement main trading loop as an `arq` worker task
- [ ] Scheduler: configure run frequency (e.g. daily pre-market)
- [ ] Sequence: expiry check → liquidity check → candidates → filter → rank → research loop → trade
- [ ] `POST /run` — trigger full trading loop manually
- [ ] `POST /evaluate` — research + evaluate a user-supplied ticker, optionally trade it
- [ ] `POST /trade` — placeholder (will be internal tool, but useful for testing)
- [ ] Set up Telegram bot with polling (no webhook)
- [ ] Whitelist-based user auth
- [ ] Commands: `/run`, `/evaluate <ticker>`, `/status` (holdings + liquidity summary), `/stop`

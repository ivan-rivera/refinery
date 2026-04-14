# Architecture

This section outlines project ambitions, mechanics and intended way to run it.

## Overview

The intention of this project is to create an autonomous swing trading bot (bets from 1-14 days long) that specialises on the precious metals market on:

* NYSE
* NYSE Acra
* NASDAQ

The bot is expected to run on a FastAPI server with a scheduled background job. This job would perform the following actions:

* Look at my current portfolio for 3 reasons:
  * First, check if any of the assets I'm holding (if I have none, we can skip this step) have reached their expiry date -- the idea is that I would have purchased these assets with a time-bound thesis in mind, and if that thesis is not met in a certain timeframe, then the assets will be sold. The bot will execute this sale if the expiry is reached.
  * Second, if some trades were triggered due to either stop-loss, take-profit or expiry rules discussed earlier. For these new trades, the bot is expected to write a brief summary on whether my thesis held up or not, and it will attempt to draw some learnings from this that it will store in global memory
  * Third, it will retain, within context, the tickers that I'm currently holding as these may drive better decisions on how to allocate any remaining funds
* Check if I have any liquidity -- if not, the process can terminate now
* If I do have funds to allocate, then it will procure candidate tickers from a range of sources such as pre-defined screeners, subreddits, global news and blogs. 
* The pipeline will run a set of basic elimination rules to narrow down the pool of candidates down
* Once we have narrowed down a set of candidates, the bot will rank them from highest potential to lowest potential, also using context directly from the sources. This ranked shortlist of tickers will enter a queue
* For each ticker in the queue, we will push it through a rigorous research phase. This phase may require multiple subagents (sentiment analyser, catalyst evaluator, technical analyst, etc) to parse the information, currate it into a report and let a supervisor agent come up with a assessment based on their findings as well as previous learnings. We want to obtain the following information about the ticker:
  * Market cap (cache: 30 days)
  * Category: Producer, Developer, Explorer, Royalty streamer (cache: 30 days)
  * Jurisdiction risk (cache: 30 days)
  * AISC (cache: 30 days)
  * Institutional baseline interest (cache: 30 days)
  * Short-term returns (3d, 7d, 14d) (cache: 1 day)
  * Volume spikes (no cache)
  * Volatility (no cache)
  * Correlation or divergence vs metal market (no cache)
  * News sentiment (no cache)
  * Social sentiment (no cache)
  * Analyst sentiment (no cache)
  * Upcoming events or catalysts (cache: 30 days)
  * Insider trades (no cache)
  * Option flows -- this one may be added later (no chache)
* Depending on the findings, the supervisor agent will pass on the recommendations to trader agent who will be able to execute a trade if trade if the findings support this decision. The trader agent will have to set a stop loss and a take profit values, together with an expiry date (the supervisor agent will pass that as a recommendation). The trader will also need to record the thesis for this trade. This agent will also need to respect some pre-configured rules, e.g. making sure that if we hit the stop loss, then we will not lose more than 2.5% of our total capital (not adjusting for slippage).
* Research findings will be cached in a database for N time units (varies per metric) -- if the same ticker comes up, we will retrieve cached results and will refresh only the fast-moving markers such as sentiment and share price.

Upon completing the above actions, the process will halt (the server will still keep running), awaiting for the next scheduled job. Additionally, the server will introduce the following endpoints:

* Enable users to run the trade loop outside of schedule
* Enable users to run a partial loop, skipping the candidate retrieval part and instead getting user to pass it a ticker that it will research and will potentially trade

With these requirements in mind, we can talk about technical requirements:

* The server will be always on. Initially it will run locally, but then it will be deployed on Railway. While it may have been preferable to have a solution like Temporal for the long-running background tasks, given the price constraints, these tasks will run within the server using `arq`.
* We will be using PydanticAI for the agentic management with an OpenRouter LLM
* Data will be pooled from multiple sources, mostly Finnhub and TwelveData. We can also pull technicals from Alpaca (the trading platform used for this project). We may also connect to Reddit and scrape some blog posts
* We need several databases for this and we will use PostgreSQL. We need tables:
  * Active holdings with metadata such as thesis, expiry, etc
  * Past trades with their learnings
  * Global journal of learnings made from trades -- these will be given to the trading agent as context
  * Cached research results
* To expose a viewable table of our standing, we will have a local Metabase server running that can access our SQL tables
* No API routes will be exposed to public, but the server will be controllable through a Telegram bot which will allow me to interact with endpoints. The server will poll Telegram bot API for requests (it will be the only _outbound_ connection). The telegram bot will have a whitelist of allowed users

# Status

This document outlines status of tasks that need to be completed.

## Tasks

### Backlog

- [ ] Create a test environment in Alpaca (human only)
- [ ] Find appropriate data sources (human only)

### Next

- [ ] Create a `/trade` endpoint placeholder
- [ ] Instantiate a PostgreSQL DB
- [ ] Under `src/services/` create `portfolio` for interacting with my portfolio
- [ ] Connect to the Alpaca API
- [ ] Implement functionality to place a trade and record expiry date plus thesis in a separate table
- [ ] Implement functionality to retrieve current ticker holdings from Alpaca and join these to relevant metadata
- [ ] Trigger a sale if expiry date is reached -- document learnings
- [ ] Implement functionality to document learnings from automatically executed trades
- [ ] Implement data sources for this project
- [ ] Implement logic to pull candidate tickers
- [ ] Implement logic to quick-filter candidate tickers
- [ ] Implement deep research logic
- [ ] Implement caching logic
- [ ] Implement guardrails
- [ ] Set up background trading job
- [ ] Create an endpoint for evaluating a specific ticker

### In Progress

- [ ] Set up harness for development

### Done

- [x] Update readme
- [x] Create docs/
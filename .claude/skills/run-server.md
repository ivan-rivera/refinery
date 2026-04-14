# Run Server

Use this skill whenever you need the local dev server running — e.g. to test an endpoint, verify a feature, or check API behaviour. The server should be treated as a temporary tool: start it, use it, stop it.

## Starting the server

Launch in the background and capture the PID so it can be cleanly stopped later:

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
```

Then wait for it to be ready before proceeding:

```bash
for i in $(seq 1 15); do
  curl -s http://localhost:8000/api/v1/health && break
  sleep 1
done
```

Note the PID — you'll need it to shut the server down.

## Stopping the server

Always stop the server when your task is complete (or if it fails):

```bash
kill $SERVER_PID 2>/dev/null
```

If the PID was lost, find and kill by port:

```bash
lsof -ti :8000 | xargs kill 2>/dev/null
```

## Lifecycle rule

Never leave the server running after the task ends. The pattern is always:
1. Start → note PID
2. Do the work
3. Stop → kill PID

I am migrating our legacy math calculation backend from Python 2 to Python 3. The system consists of a Node.js API gateway, a Redis message broker, and a Python worker that parses and evaluates custom prefix-notation math expressions.

Unfortunately, the original Python 2 source code for the worker was lost. We only have a compiled reference binary of the old worker at `/home/user/app/oracle_worker`. We need you to write a drop-in Python 3 replacement.

Here is what you need to do:

1. **Fix the Multi-Service Integration**: 
   The Node.js gateway (`/home/user/app/gateway.js`) and startup script (`/home/user/app/start.sh`) are currently misconfigured. The gateway is trying to connect to Redis on port 6380 instead of the default 6379, and it is pushing to the wrong queue (`old_jobs` instead of `math_jobs`). Fix `gateway.js` so it connects to Redis correctly and uses the `math_jobs` queue for tasks and `math_results` for answers. Start the services using `./start.sh`.

2. **Implement the Python 3 Worker**:
   Create `/home/user/app/worker.py`. It must serve two modes:
   - **Service Mode** (run without arguments): It should continuously `BLPOP` from the `math_jobs` Redis queue. The payload from Redis is a JSON string: `{"id": "...", "payload": "<base64_encoded_expression>"}`. It must decode the base64 payload, parse and evaluate the math expression, and then `LPUSH` the integer result to the `math_results` queue as a JSON string: `{"id": "...", "result": <integer>}`.
   - **CLI Mode** (run with `--cli <base64_encoded_expression>`): For testing, it must decode the expression, evaluate it, print the integer result to stdout, and exit.

3. **Parser & Math Semantics**:
   The custom math format uses a Lisp-like prefix notation, e.g., `(ADD (MUL 3 4) (SUB 10 2))`.
   - Supported operations: `ADD`, `SUB`, `MUL`, `DIV`.
   - Data types: 32-bit signed integers.
   - **Crucial Python 2 Migration Detail**: The old worker was written in Python 2. The `DIV` operation relies strictly on Python 2's integer division semantics (floor division). Your Python 3 implementation must replicate this behavior exactly, including how it handles negative numbers.

Verify your implementation by ensuring `curl -X POST -H "Content-Type: application/json" -d '{"expr": "(DIV -10 3)"}' http://localhost:8080/calc` returns `{"result": -4}`, matching Python 2 logic.
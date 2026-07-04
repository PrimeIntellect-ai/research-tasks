I am migrating my mathematical evaluation pipeline from Python 2 to Python 3. The pipeline consists of a Python-based WebSocket server that evaluates math expressions, and a Bash build/test system. 

I need you to fix the build/test scripts and write a robust Bash client to interface with the newly migrated server.

Here is what you need to do:

1. **Update the Runner Script**: 
   I have a script at `/home/user/start_server.sh`. Modify it so that it accepts a `--py3` flag. 
   - If `--py3` is passed, it should run `/home/user/math_server.py` using `python3`.
   - Otherwise, it should default to `python2`.
   - Ensure the server runs in the background and give it 2 seconds to start.

2. **Write the Bash WebSocket Client (`/home/user/ws_client.sh`)**:
   Create a Bash script that acts as the client. It must:
   - Read expressions line-by-line from `/home/user/expressions.txt`.
   - Send each expression to the WebSocket server running at `ws://127.0.0.1:8888`. You can use `websocat` to communicate with the server (e.g., by echoing the expression and piping it to `websocat -1 ws://127.0.0.1:8888`).
   - Read the server's response. 
   - **Fallback Parsing**: During our migration, the Python 3 server sometimes fails on legacy floating-point divisions and returns the exact string `MIGRATION_ERROR`. If the server returns `MIGRATION_ERROR`, your Bash script must parse and evaluate the math expression locally using `bc -l`.
   - Format the final output as: `[Expression] = [Result]`
   - Append each formatted line to `/home/user/evaluation_results.log`.
   - Strip any trailing newlines or whitespace from the result. For local evaluations using `bc -l`, format the output to preserve `bc`'s default scale but strip leading zeros if `bc` omits them (just raw `bc -l` output is fine).

3. **Execution**:
   - Stop any currently running `math_server.py` instances.
   - Run the modified `/home/user/start_server.sh` with the `--py3` flag.
   - Run your `/home/user/ws_client.sh` script to process `/home/user/expressions.txt`.

Ensure `/home/user/evaluation_results.log` is perfectly formatted before finishing the task.
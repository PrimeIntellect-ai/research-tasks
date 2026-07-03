You are tasked with building the core of a custom, polyglot CI/CD runner named "PolyRunner". Your goal is to create a Python-based local build system that parses a custom domain-specific language (DSL), translates it into executable scripts (Python or Bash), and coordinates build jobs via WebSockets.

Perform all work inside `/home/user/polyrunner`. Create the directory if it does not exist.

Phase 1: State Machine & Code Translator
Create a file `/home/user/polyrunner/translator.py`. It must contain a function `translate(filepath)` that reads a `.polybuild` file and returns a tuple: `(target_language, translated_code_string)`.
You must implement the parser as a Finite State Machine (FSM) reading the file line by line.

The `.polybuild` DSL has the following structure and strict sequence:
1. `TARGET <lang>` (where `<lang>` is either `python` or `bash`)
2. `BEGIN_PSEUDO`
3. One or more pseudo-code statements:
   - `PRINT "<string>"` (e.g., `PRINT "Starting build"`)
   - `SET_VAR <var_name> <value>` (e.g., `SET_VAR version 5`)
   - `PRINT <var_name>` (e.g., `PRINT version`)
4. `END_PSEUDO`

Translation rules:
- `TARGET python`: `PRINT "<string>"` -> `print("<string>")`; `SET_VAR x 5` -> `x = 5`; `PRINT x` -> `print(x)`
- `TARGET bash`: `PRINT "<string>"` -> `echo "<string>"`; `SET_VAR x 5` -> `x=5`; `PRINT x` -> `echo $x`

Phase 2: WebSocket Runner
Create a file `/home/user/polyrunner/server.py`. It must run a WebSocket server on `localhost:9333` using the `websockets` and `asyncio` libraries.
- When a client connects and sends a JSON message `{"action": "build", "file": "<absolute_path_to_polybuild_file>"}`, the server must:
  1. Call `translate()` on the file.
  2. Save the translated code to a temporary file (either `.py` or `.sh`).
  3. Execute the file using `subprocess` (use `python3` for python target, `bash` for bash target).
  4. Capture the standard output of the execution.
  5. Send back a JSON response to the WebSocket client: `{"status": "success", "output": "<captured_stdout_stripped_of_surrounding_whitespace>"}`.

Phase 3: CI/CD Pipeline Setup
Create a shell script `/home/user/polyrunner/ci_setup.sh`. This script will act as a mock CI bootstrap script.
It must:
1. Install the `websockets` Python package (e.g., via `pip`).
2. Start the `server.py` in the background (ensuring it runs).
3. Wait 2 seconds for the server to bind.
4. Exit with code 0.

Write robust code. Ensure the server gracefully handles the JSON parsing and executes the output code correctly. Do not use any external translation libraries, the FSM must be your own logic.
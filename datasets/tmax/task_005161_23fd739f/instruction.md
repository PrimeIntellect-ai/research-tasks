You are an AI assistant helping a developer organize and analyze legacy project activity logs. The developer has a set of custom log files with the `.actlog` extension. Your task is to build a strict state-machine parser for these files, benchmark its performance, and expose the parsed data via a REST API.

**Background: The `.actlog` Format**
The `.actlog` files contain records of developer actions on various project files. The format is strict and must be parsed line-by-line using a state machine (do not use regular expressions for block extraction).
Rules:
1. Lines starting with `#` are comments and should be ignored.
2. Empty lines should be ignored.
3. A block starts with a line strictly formatted as `BEGIN <project_name>` (e.g., `BEGIN AuthModule`).
4. Inside a block, lines can be `ACTION <action_name>` followed by `FILE <file_path>`. There can be multiple ACTION/FILE pairs in a single block. An `ACTION` must always be immediately followed by a `FILE`.
5. A block ends with the exact line `END`.
6. Any malformed sequence (e.g., `FILE` without a preceding `ACTION`, or `BEGIN` inside another `BEGIN`) should cause the parser to raise a `ValueError`.

**Phase 1: State Machine Parser**
Create a Python file at `/home/user/parser.py`.
It must contain a class `ActLogParser`.
It must have a method `parse(filepath: str) -> dict` that reads the file line-by-line and returns a dictionary where keys are project names, and values are lists of dictionaries containing the actions and files.
Example output format:
```python
{
  "AuthModule": [
    {"action": "refactor", "file": "src/auth.py"},
    {"action": "test", "file": "tests/test_auth.py"}
  ]
}
```

**Phase 2: Performance Benchmarking**
There is a large log file located at `/home/user/large.actlog`.
Create a script at `/home/user/benchmark.py` that:
1. Imports your `ActLogParser`.
2. Records the start time using `time.perf_counter()`.
3. Parses `/home/user/large.actlog` exactly 50 times in a loop.
4. Records the end time.
5. Calculates the average time per parse (total time / 50).
6. Writes ONLY the average time as a floating-point number to `/home/user/bench_result.txt`.

**Phase 3: REST API**
Create a REST API using FastAPI in `/home/user/api.py`.
The API should instantiate your parser, parse `/home/user/data/project.actlog` ONCE at startup, and keep the data in memory.
The API must run on `0.0.0.0` at port `8000`.

Endpoints to implement:
1. `GET /projects`
   Returns a JSON list of all project names found in the log file.
2. `GET /actions/{project_name}`
   Returns a JSON list of the actions and files for the specified project (matching the list format described in Phase 1). If the project does not exist, return a 404 status code with `{"detail": "Project not found"}`.

**Instructions:**
1. You may need to install `fastapi` and `uvicorn`.
2. Write the parser, benchmarking script, and API server.
3. Run the benchmark script to generate `/home/user/bench_result.txt`.
4. Start the FastAPI server in the background so it is actively listening on port 8000 when you complete the task.
5. Do not use regex for the parser logic. Use standard string operations (`startswith`, `split`, etc.) and maintain a state variable (e.g., `WAITING`, `IN_BLOCK`, `EXPECTING_FILE`).
We are porting an older, proprietary C-based log parsing and metric calculation tool to a minimal Python container environment. You need to accomplish two goals to complete this migration.

**Part 1: Fix and Install the Vendored Dependency**
We rely on a specific state machine library that has been vendored at `/app/vendored/pysm-lib`. However, the `pip install /app/vendored/pysm-lib` command currently fails due to conflicting peer dependencies specified in its `setup.py` (it erroneously requests two incompatible versions of `typing-extensions`). 
1. Identify and fix the dependency conflict in the `setup.py` of the vendored package.
2. Successfully install the package into the system Python environment.

**Part 2: Reimplement the Legacy Parser**
We have a legacy compiled binary located at `/app/oracle/legacy_parser` (which has been provided for you to test against). We need a Python equivalent written to `/home/user/new_parser.py`.

The parser reads a stream of text commands from standard input (`stdin`), processes them using a state machine, and writes the results to standard output (`stdout`). 

You must reverse-engineer the exact behavior of `/app/oracle/legacy_parser`. To help you, here are the basic rules of its numerical state machine:
- It starts in the `IDLE` state.
- `INIT <integer>`: Transitions to `ACTIVE` state, setting the internal accumulator to the provided integer.
- `ADD <integer>`: If `ACTIVE`, adds the integer to the accumulator.
- `MUL <integer>`: If `ACTIVE`, multiplies the accumulator by the integer.
- `EMIT`: If `ACTIVE`, prints `RESULT: <accumulator>` to `stdout` (with a newline) and transitions back to `IDLE`.
- If `ADD`, `MUL`, or `EMIT` are encountered while in the `IDLE` state, it prints `ERROR: INVALID_STATE` to `stdout`.
- Unknown commands or poorly formatted lines should print `ERROR: UNKNOWN_CMD`.

Your Python script (`/home/user/new_parser.py`) must be **bit-exact equivalent** to the legacy binary. It must handle all edge cases, multiple consecutive operations, and identical error messages exactly as `/app/oracle/legacy_parser` does. 

We will verify your solution by generating thousands of random input sequences and asserting that the `stdout` from your `/home/user/new_parser.py` is identical to `/app/oracle/legacy_parser` for every single input.
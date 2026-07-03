You are a QA Engineer setting up a test environment for a legacy data processing Python package called `log_processor`. The package is in a broken state, and you need to fix its build system, implement missing parsing and migration logic, and process a test log file.

The project is located at `/home/user/log_processor`.

Your tasks are:

1. **Fix the Build System (Conditional Compilation)**
   The `setup.py` file in `/home/user/log_processor` is incomplete and broken. Fix it so that it uses `setuptools`. 
   Crucially, the package contains a C-extension at `src/log_processor/_fast_ext.c`. You must configure `setup.py` to compile this extension (as `log_processor._fast_ext`) **ONLY IF** the environment variable `ENABLE_C_EXT=1` is set during installation. If the variable is not set or equals 0, it should install purely as a standard Python package without attempting to build the C-extension.
   Ensure the package can be installed in editable mode (`pip install -e .`).

2. **Implement the State Machine Parser**
   The file `/home/user/log_processor/src/log_processor/parser.py` contains an empty function `parse_logs(file_path: str) -> list[dict]`. Implement a state machine to parse a legacy multiline log format.
   The log format rules:
   - A transaction begins with `BEGIN tx=<tx_id>`
   - Followed by zero or more attribute lines: `ATTR <key>=<value>`
   - Ends with `END`
   - Ignore any lines outside of a `BEGIN` ... `END` block, or any lines inside a block that don't match the `ATTR` or `END` pattern.
   - The output for each transaction should be a dictionary: `{"tx": "<tx_id>", "<key1>": "<value1>", "<key2>": "<value2>"}`.

3. **Implement Schema Migration**
   The file `/home/user/log_processor/src/log_processor/migrator.py` contains an empty function `migrate_schema(records: list[dict]) -> list[dict]`. 
   Migrate the parsed dictionaries to a v2 schema:
   - Rename the `tx` key to `transaction_id` and convert its value to an integer.
   - Add a static field `"schema_version": 2`.
   - Take all other arbitrary keys from the parsed dictionary and nest them inside a new dictionary under the key `"properties"`.
   Example Input: `{"tx": "105", "user": "admin", "action": "login"}`
   Example Output: `{"transaction_id": 105, "schema_version": 2, "properties": {"user": "admin", "action": "login"}}`

4. **Process the Logs**
   A raw log file is located at `/home/user/raw_data.log`.
   Write a script at `/home/user/run_pipeline.py` that imports `parse_logs` and `migrate_schema` from the `log_processor` package, reads `/home/user/raw_data.log`, processes the records, and writes the output as a JSON Lines file to `/home/user/migrated_output.jsonl`. Each line must be a valid JSON object.

Install the package in the environment (using `pip install -e .` with the C-extension disabled) before running your script.
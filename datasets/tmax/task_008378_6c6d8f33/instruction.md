You are an open-source maintainer reviewing a pull request for a Python package called `numsock`. This package runs a WebSocket server that receives numbers, calculates a running Exponential Moving Average (EMA), and stores the results in a SQLite database. The PR author left the repository in a broken state.

Your task is to fix the repository, start the server, test it, and output the final database state.

The repository is located at `/home/user/numsock_repo/`.

Here are the issues you must resolve:
1. **Broken Packaging**: The `pyproject.toml` file is malformed and missing the `websockets` dependency. Fix it so the package can be installed in editable mode (`pip install -e .`).
2. **Broken Schema Migration Patch**: The PR includes a patch file `/home/user/numsock_repo/pr_migration.patch` intended to update `numsock/db.py` to schema version 2 (adding the `ema` column to the database). The patch contains a SQL syntax error (`FLOATX` instead of `FLOAT`) and won't apply cleanly. Fix the patch or manually apply its intent to `numsock/db.py`, then run the migration to create `/home/user/numsock_repo/data.db`.
3. **Broken Algorithm & WebSockets**: Modify `/home/user/numsock_repo/numsock/server.py`. 
   - Fix the WebSocket receive loop to correctly parse incoming JSON like `{"value": 10.0}`.
   - Implement the correct EMA algorithm. The EMA formula is: `EMA_today = (Value_today * alpha) + (EMA_yesterday * (1 - alpha))`. Use `alpha = 0.5`. For the very first value received, the EMA is exactly that value.
   - Ensure the server inserts the `value` and calculated `ema` into the `data.db` database using the `insert_record` function from `db.py`.
   - Send back a JSON response `{"ema": <calculated_ema>}` over the WebSocket.

Once the code is fixed:
1. Start the WebSocket server (it binds to `localhost:8765`).
2. Run the provided test client: `python /home/user/numsock_repo/test_client.py`.
3. After the test client finishes, dump the contents of the `records` table from `/home/user/numsock_repo/data.db` into a JSON file at `/home/user/final_result.json`.

The `final_result.json` must be an exact JSON array of dictionaries, where each dictionary represents a row with keys `"id"`, `"value"`, and `"ema"`. All numeric values should be floats.
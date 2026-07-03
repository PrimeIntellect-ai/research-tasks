You are a platform engineer responsible for maintaining the CI/CD pipeline for a data processing service called "MathApp". The service has a polyglot architecture: a Python frontend interacting with an SQLite database and a high-performance C extension for mathematical computations. 

Currently, the CI pipeline is failing due to three issues: the C extension build is broken, the database schema needs a migration, and the data processing script needs to be updated and run.

Your objective is to fix the build, migrate the database schema, and process a new batch of data.

Here is the current state of `/home/user/math_app`:
1. `mathcore.c`: A C Python extension that calculates the square root of a double using the standard C math library.
2. `setup.py`: The build script for the C extension. It currently fails to compile/link correctly in the CI environment because it does not explicitly link the required C math library.
3. `data.db`: An SQLite database with an existing table containing legacy calculations.
   - Old Schema: `CREATE TABLE calculations (id INTEGER, result REAL);`

**Step 1: Fix the Polyglot Build**
Modify `/home/user/math_app/setup.py` so that the `mathcore` extension successfully compiles and links against the necessary system libraries. Build and install the extension in the current Python environment (using `python3 setup.py build_ext --inplace` or similar).

**Step 2: Schema Migration**
Write a Python script `/home/user/math_app/migrate.py` to migrate the `data.db` SQLite database to the new schema while preserving existing data.
- New Schema: `CREATE TABLE calculations_new (id INTEGER PRIMARY KEY, input_val REAL, result REAL, algo_version TEXT);`
- For all existing legacy rows, map `id` to `id`, `result` to `result`. Since the original inputs are unknown, set `input_val` to `0.0` and `algo_version` to `'1.0'` for these legacy rows.
- Drop the old table and rename the new table to `calculations`.

**Step 3: Execute and Log Results**
Write a Python script `/home/user/math_app/run.py` that does the following:
1. Imports your newly compiled `mathcore` module.
2. Uses `mathcore.fast_sqrt(value)` to calculate the square roots for the following float values: `16.0`, `64.0`, and `144.0`.
3. Inserts these new calculations into the migrated `data.db` database. For these new rows, store the input values appropriately, store the computed square roots in `result`, and set `algo_version` to `'2.0'`. Let SQLite auto-increment the `id`.
4. Queries all rows from the `calculations` table (ordered by `id` ascending) and dumps them to a JSON file at `/home/user/final_data.json`.

The JSON file must be a list of dictionaries, for example:
```json
[
  {"id": 1, "input_val": 0.0, "result": 9.0, "algo_version": "1.0"},
  ...
]
```

Ensure all scripts are executable or can be run directly with `python3`. Your final output for verification will be the presence and correct formatting of `/home/user/final_data.json`.
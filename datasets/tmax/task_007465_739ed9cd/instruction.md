You are a mobile build engineer responsible for maintaining our automated build pipelines. The pipeline for our mobile application has broken during the pre-build asset generation phase. We need you to repair the build process, perform a database schema migration, and calculate required numerical metrics.

Here is the context and your requirements:

Our mobile app ships with a pre-populated local SQLite database containing calibration metrics. The old database format (`v1.db`) is located at `/home/user/mobile_build/data/v1.db`.

You need to perform the following steps to fix the pipeline:

1. **Fix the Rust Signer Tool**
   The pipeline uses a custom Rust tool to generate simple signature files for our build artifacts. The source code is located in `/home/user/mobile_build/tools/db_signer/`.
   Currently, the tool fails to compile due to a Rust ownership and borrow checker error. 
   - Debug and fix the borrow checker issue in `/home/user/mobile_build/tools/db_signer/src/main.rs`. 
   - Ensure you do not change the intended logic or the output format of the signature.
   - Build the tool using `cargo build --release` from the tool's directory.

2. **Implement the Migration and Numerical Algorithm**
   We need to migrate `v1.db` to a new schema (`v2.db`) and compute a smoothed metric using an Exponential Moving Average (EMA).
   Create a Python script at `/home/user/mobile_build/scripts/migrate.py` that does the following:
   - Connects to `/home/user/mobile_build/data/v1.db` and reads all records from the `raw_metrics` table. The table has the schema: `(id INTEGER PRIMARY KEY, ts INTEGER, val REAL)`.
   - Creates a new SQLite database at `/home/user/mobile_build/data/v2.db` with a table named `metrics_v2` having the schema: `(id INTEGER PRIMARY KEY, ts INTEGER, val REAL, ema REAL)`.
   - Processes the records ordered strictly by the `ts` column (ascending).
   - Computes the EMA for each row using the formula:
     `EMA_current = (val_current * alpha) + (EMA_previous * (1 - alpha))`
     where `alpha = 0.25`.
     *Note: For the chronologically first record, `EMA_current` should simply equal its `val_current`.*
   - Inserts the resulting data (including the computed EMA) into the `metrics_v2` table.

3. **Generate the Signature Artifact**
   Once `v2.db` is successfully generated, run the compiled Rust signer tool on the new database to generate the final artifact signature.
   Execute:
   `/home/user/mobile_build/tools/db_signer/target/release/db_signer /home/user/mobile_build/data/v2.db`
   This will automatically create a file named `/home/user/mobile_build/data/v2.db.sig`.

Ensure all file paths match exactly as specified. Do not modify the data in `v1.db`.
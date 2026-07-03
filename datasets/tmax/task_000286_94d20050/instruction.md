You are an on-call engineer receiving a PagerDuty alert at 3 AM. The nightly financial data processing pipeline has failed, and the downstream trading system is blocked. 

The pipeline runs via a shell script located at `/home/user/pipeline.sh`. It executes a Python script `/home/user/process_data.py` that calculates the Exponential Moving Average (EMA) of stock prices stored in a SQLite database (`/home/user/data.db`).

The pipeline is suffering from multiple issues:
1. The shell script (`pipeline.sh`) is failing to execute properly due to a bug in how it sets up and runs the job.
2. The Python script is crashing or returning wrong results because of an incorrect SQL query (query result debugging).
3. The EMA mathematical formula in the Python script was recently modified by a junior developer and is calculating incorrect values (formula implementation correction).

Your task:
1. Diagnose and fix the build/execution failure in `/home/user/pipeline.sh`.
2. Fix the SQL query in `/home/user/process_data.py` so that data is processed in the correct chronological order (oldest to newest). The table name in the database is `daily_prices`, and it has columns `date` and `price`.
3. Fix the EMA formula in `calculate_ema`. The standard formula should be: `EMA = (Current Price * alpha) + (Previous EMA * (1 - alpha))`.
4. Run `/home/user/pipeline.sh` successfully. The script should output the final calculated EMA value to `/home/user/final_ema.txt` rounded to 4 decimal places.

Do not change the `alpha` value (0.1) or the output format. Fix the bugs and ensure `/home/user/final_ema.txt` contains only the correct final EMA value.
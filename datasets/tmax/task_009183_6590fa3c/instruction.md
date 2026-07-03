You have inherited an unfamiliar codebase located at `/home/user/sensor_pipeline`. The previous developer left behind a data processing pipeline that reads sensor data from CSV files, calculates the mean and variance, and outputs a JSON summary.

However, the pipeline is currently broken:
1. The wrapper script `/home/user/sensor_pipeline/run_pipeline.sh` fails to process certain files in the `data/` directory. You suspect it breaks on filenames with spaces.
2. The Python script `/home/user/sensor_pipeline/process.py` crashes intermittently with a `ValueError: math domain error` (or outputs `NaN`/negative variance) when calculating the standard deviation for certain datasets. This is due to numerical instability (catastrophic cancellation) in the naive variance calculation.
3. According to some old notes, a robust algorithm (Welford's algorithm) was implemented by a former team member to fix this numerical instability, but it seems to have been lost or reverted in the Git history.

Your tasks are to:
1. Fix `run_pipeline.sh` so it correctly iterates over and passes all `.csv` files in the `data/` directory to `process.py`, regardless of spaces in their names.
2. Recover the Welford algorithm implementation from the repository's Git history and apply it to `process.py` to fix the numerical instability.
3. Run the fixed `run_pipeline.sh` and redirect its complete combined JSON output to `/home/user/results.json`. The output should be a single valid JSON object mapping each filename (just the basename, e.g., "sensor A.csv") to its `mean` and `variance`.
4. Identify the full 40-character Git commit hash of the commit that originally introduced the Welford algorithm. Write this hash into a new file at `/home/user/recovery_info.txt`.

Ensure `/home/user/results.json` and `/home/user/recovery_info.txt` are created exactly as specified. Do not change the underlying mathematical intent (it calculates population variance), just fix the numerical stability and string handling.
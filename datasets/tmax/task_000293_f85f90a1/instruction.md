You are a data analyst tasked with processing irregular IoT sensor logs into a clean, resampled master dataset. 

You have been provided with a directory of raw CSV files at `/home/user/data/raw/`. These files:
- Are encoded in `ISO-8859-1`.
- Contain two columns: `timestamp` (Unix epoch seconds) and `temperature` (float).
- Have irregular timestamps and missing readings.

Your organization uses a custom, vendored toolkit for timeseries interpolation located at `/app/awk-ts-tools-1.0`. 
However, the toolkit is currently broken. Your multi-stage task is as follows:

1. **Fix the Vendored Toolkit:** 
   Inspect `/app/awk-ts-tools-1.0`. The core interpolation script (`interpolate.awk`) contains a mathematical bug in its linear interpolation logic for gap-filling, and the `Makefile` has a misconfigured environment variable preventing it from running properly. Fix the bug and ensure the toolkit is usable.

2. **Develop the Pipeline Script:**
   Create a bash script at `/home/user/pipeline.sh` that performs the following multi-stage extraction and transformation using coreutils and the fixed toolkit:
   - Reads all CSV files in `/home/user/data/raw/`.
   - Converts their character encoding from `ISO-8859-1` to `UTF-8`.
   - Resamples the data to exact 60-second (1-minute) intervals, starting from the earliest timestamp present in the data up to the latest.
   - Uses the fixed `/app/awk-ts-tools-1.0/interpolate.awk` to linearly interpolate any missing temperature values for the 60-second intervals.
   - Appends the final, sorted, gap-filled data to `/home/user/data/processed/master.csv` (format: `timestamp,temperature`).

3. **Schedule the Pipeline:**
   Configure the system's crontab for the `user` to run `/home/user/pipeline.sh` every 15 minutes.

Your final output `/home/user/data/processed/master.csv` will be graded based on the Mean Squared Error (MSE) of your interpolated temperature values against a hidden ground-truth dataset. High accuracy is critical!
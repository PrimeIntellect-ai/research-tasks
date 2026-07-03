You are acting as a data analyst. I have a raw data file from our sensors at `/home/user/sensor_data.csv`. I previously wrote a bash pipeline to calculate the Pearson correlation coefficient between the two sensor readings, but it keeps returning `NaN` or failing entirely because the CSV file contains malformed data and schema violations.

Your task is to fix this by writing a robust Bash-only pipeline (using standard CLI tools like `awk`, `grep`, `sed`, `bc`, etc. - no Python or R allowed) to do the following:

1. **Schema Enforcement**: Filter the raw data so that only valid rows are kept. Save the valid rows to `/home/user/clean_data.csv`. 
   A valid row must strictly meet these requirements:
   - Exactly three columns, separated by commas.
   - Column 1 (timestamp): Alphanumeric string.
   - Column 2 (Sensor_A): A valid integer or floating-point number.
   - Column 3 (Sensor_B): A valid integer or floating-point number.
   - The header row (`timestamp,sensor_A,sensor_B`) should be preserved as the first line of the clean file.

2. **Numerical Accuracy & Correlation**: Read the cleaned dataset and calculate the Pearson correlation coefficient ($r$) between Sensor_A and Sensor_B.
   - You must handle the floating-point math carefully (e.g., using `awk` or `bc -l`).
   - Round the final correlation value to exactly 4 decimal places.
   - Save ONLY the single numerical value (e.g., `0.8523`) to `/home/user/correlation.txt`.

Do not use any external scripting languages like Python, Perl, or Ruby. Only use Bash built-ins and standard POSIX/Linux coreutils.
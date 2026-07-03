You are an IT support technician responding to an escalated ticket (Ticket #9921). 

A backend team has a custom Bash script, `/home/user/calc_variance.sh`, which parses database query results from a CSV file and calculates the population variance of the readings for a specific sensor. 

The team has reported two major issues when running it against the latest daily dump (`/home/user/daily_query.csv`):
1. **Format Parsing Crash:** The script frequently crashes with a syntax error (e.g., `operand expected`) before finishing. The team suspects there are edge cases in the query results (e.g., corrupted or missing values) that the bash read loop isn't handling.
2. **Numerical Instability:** When they tested the script on a cleaned, smaller version of the file, it sometimes output a **negative variance** or wildly incorrect numbers. They suspect an arithmetic overflow or numerical instability, as the sensor values are consistently large (in the millions).

Your objectives are:
1. **Fuzz / Isolate the Parsing Bug:** Identify the exact line number in `/home/user/daily_query.csv` that contains the malformed value causing the bash syntax error. Write ONLY this line number to a file named `/home/user/buggy_line.txt`.
2. **Fix the Script:** Modify `/home/user/calc_variance.sh` so that it:
   - Gracefully ignores any lines where the value is empty, non-numeric, or malformed.
   - Calculates the variance without overflowing or suffering from integer limits (you may use standard tools like `awk` or `bc` within the bash script).
   - Still accepts the input file as the first argument (`$1`) and the sensor name as the second argument (`$2`).
   - Prints ONLY the final computed variance (as an integer, rounded down to the nearest whole number) to standard output.

**Execution Context:**
The script is run like this: `./calc_variance.sh /home/user/daily_query.csv SENSOR_X`
The CSV format is: `timestamp,sensor_name,value` (no header).

Ensure your fixed script is robust and correctly computes the variance. Once you have saved your fixed script and created `/home/user/buggy_line.txt`, you are done.
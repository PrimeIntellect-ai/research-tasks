You are acting as a data analyst for a web infrastructure company. You have been provided with an ETL pipeline script, `/home/user/analytics.py`, that processes server log CSV files from `/home/user/data/`, performs an independent t-test to compare the `response_time` of `Server_A` and `Server_B`, and generates a histogram plot.

However, the script is currently broken due to a few issues:
1. **Schema Enforcement**: One of the logs contains malformed data in the `response_time` column, causing pandas to interpret it as a string instead of a float. This breaks the statistical testing.
2. **Backend Misconfiguration**: The script tries to generate a plot using matplotlib, but it explicitly uses an interactive backend (`TkAgg`). Since you are running in a headless Linux terminal without a display, this will crash.

Your tasks are to:
1. Fix `/home/user/analytics.py` so that it correctly coerces the `response_time` column to numeric values (handling errors by dropping rows with invalid `response_time` values).
2. Fix the matplotlib backend issue so that the script successfully saves the plot to `/home/user/report.png` without crashing. You should use a headless backend.
3. Run the script. Ensure it outputs a file named `/home/user/results.json` containing the calculated t-statistic and p-value. The output JSON must have exactly the following keys: `{"t_stat": <float>, "p_value": <float>}`.

Do not change the statistical test being performed (independent t-test). All data files are located in `/home/user/data/`.
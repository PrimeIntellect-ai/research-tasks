You are a data scientist cleaning a noisy log dataset to analyze API performance. 

Your tasks are to:
1. Transfer the data: A local server is hosting a raw log file. Start a Python HTTP server on port 8080 in the `/home/user/server` directory. Then, write a script to download `http://localhost:8080/logs.txt` and save it to `/home/user/workspace/logs.txt`.
2. Clean and Extract: Parse `/home/user/workspace/logs.txt` using Python. Use regex to extract the duration in milliseconds from lines containing the pattern `Duration: <number>ms` (e.g., `Duration: 45ms`). Ignore any lines where the duration is not a valid integer (e.g., `Duration: N/Ams`). 
3. Compute Rolling Statistics: Maintain a list of the chronologically extracted valid durations. Calculate a rolling average of these valid durations using a window size of 3. (For the first and second valid values, average the 1 or 2 available values respectively. From the third value onwards, average the current value and the two immediately preceding valid values).
4. Compute Summary Statistics: Determine the overall minimum and maximum of the valid durations.
5. Save Results: Create a JSON file at `/home/user/workspace/summary.json` containing the overall summary statistics and the very last computed rolling average.

The JSON should have the exact following schema:
```json
{
  "min": <integer>,
  "max": <integer>,
  "final_rolling_avg": <float rounded to 2 decimal places>
}
```

Ensure all paths are absolute and the JSON output matches the requested keys exactly.
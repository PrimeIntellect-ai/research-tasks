You are a log analyst investigating a recent wave of targeted attacks. We have collected a set of raw web server logs in `/app/data/logs/`. However, the collection pipeline was misconfigured, resulting in logs with mixed character encodings (UTF-8, UTF-16LE, and ISO-8859-1) and mismatched timestamp formats. 

Your objective is to build a Bash-based data processing pipeline that cleans the data and computes a rolling 5-minute windowed count of HTTP 404 errors using our custom high-performance aggregator tool.

Here are your instructions:
1. **Fix the Aggregator Tool**: We use a custom C utility located at `/app/vendored/window_agg/`. It reads `timestamp,status_code` (comma-separated, one per line) from stdin and outputs `window_start,count` for a given window size in seconds. However, its `Makefile` was accidentally broken in the last commit, preventing it from compiling. Fix the `Makefile` and compile the tool.
2. **Normalize Encodings**: Write a Bash pipeline that reads all `.log` files in `/app/data/logs/`, detects their character encoding (or attempts standard conversions), and normalizes them all to standard UTF-8. 
3. **Parse and Align Timestamps**: The logs contain timestamps in different string formats (e.g., `YYYY-MM-DD HH:MM:SS` and `DD/MMM/YYYY:HH:MM:SS`). Use Bash (with standard GNU tools like `awk`, `sed`, or `date`) to parse these and align them into standard UNIX epoch timestamps. Deduplicate any exact duplicate log lines.
4. **Aggregate**: Pipe the normalized, deduplicated stream of `<epoch_timestamp>,<status_code>` into the fixed aggregator tool with a window size of `300` (5 minutes). 
5. **Output**: Save the final aggregated output (which should just be lines of `epoch_timestamp,404_count`) to `/home/user/aggregated_404s.csv`. The output must be sorted chronologically.

Your final results in `/home/user/aggregated_404s.csv` will be evaluated programmatically against a strictly clean reference dataset. A small margin of error (MSE) is allowed for edge cases in timestamp boundaries, but your pipeline's output must closely match the ground truth.
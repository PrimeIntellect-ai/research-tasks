You are a support engineer tasked with collecting diagnostics for a sudden reporting failure. 

Earlier today, a colleague accidentally deleted a critical script located at `/home/user/report.py`. Fortunately, an instance of this script is still running (hanging or sleeping) in the background. 

Your tasks are:
1. **Recover the deleted file**: Inspect the filesystem to recover the source code of the deleted `report.py` script from the running process.
2. **Debug the query**: The recovered script queries an SQLite database (`/home/user/events.db`) to find events that occurred on the calendar day `2024-05-01` in the `US/Eastern` timezone. However, the database stores `event_time` in UTC (ISO 8601 format), and the original script has a subtle bug: it naively filters using UTC string matching, causing it to return incorrect results for the US/Eastern day.
3. **Create a minimal reproducible example**: Write a fixed, minimal script at `/home/user/minimal_repro.py` (in any language you choose) that connects to `/home/user/events.db`, correctly filters the events for the `2024-05-01` calendar date in `US/Eastern` time, and writes the correct integer IDs of the matching events.

Write the matching IDs to `/home/user/correct_ids.txt`, with one integer ID per line, sorted in ascending order.
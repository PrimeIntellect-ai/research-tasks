You are assisting a compliance officer auditing an organization's physical access control systems. 

We have a SQLite database located at `/app/access_logs.db`. The database contains multiple tables tracking employee badge scans and access points. Currently, the Python script used for generating access reports (`/app/generate_report.py`) is producing massively inflated access counts due to a suspected implicit cross join in its SQL query when correlating badge scans with camera events.

Additionally, our camera system recently went offline, and we only have a raw surveillance video at `/app/surveillance.mp4` covering the main entrance for today. The video has timestamp overlays and a visual indicator (a solid red rectangle in the top-right corner) whenever the door actually opens. 

Your task is to:
1. Reverse engineer the data model in `/app/access_logs.db`.
2. Write a Python script to process `/app/surveillance.mp4` using `ffmpeg` or `cv2`, extract the timestamps (in seconds from the start of the video) where the door is open (red rectangle present), and insert these events into the database's `camera_events` table.
3. Fix the logical flaw (the implicit cross join) in the reporting query so that a badge scan is only correlated with a camera event if they occurred at the same `door_id` within a 5-second window.
4. Create a final parameterized script at `/home/user/audit_query.py` that takes three arguments: `badge_id`, `start_time`, and `end_time`. This script must execute the fixed SQL pipeline, aggregate the valid access events for that user in that time window, and print exactly a single integer representing the valid access count to standard output.

Ensure your script handles edge cases and imports standard data query libraries correctly. Our automated test suite will aggressively fuzz your `/home/user/audit_query.py` script with various parameters to ensure it matches the correct, optimized logic.
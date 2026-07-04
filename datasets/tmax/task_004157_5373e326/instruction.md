You are acting as a Database Administrator investigating a recent database incident. Our main SQLite database (`/home/user/system.db`) has been returning stale rows and experiencing severe performance degradation due to what we suspect is a corrupted index on the `events` table. Additionally, our application has been receiving malicious or unoptimized query payloads from an upstream service.

We also have a security camera recording of the server rack (`/app/server_rack.mp4`). We suspect a physical server glitch occurred. The video contains occasional flashes (all-white frames) indicating a hardware reset.

Your task consists of three phases:

Phase 1: Video Correlation
Extract the exact frame numbers of all the "white flash" events (where the average frame luminance is > 95%) from `/app/server_rack.mp4`. Use `ffmpeg` to extract frames if needed. Save the sorted list of frame numbers, one per line, to `/home/user/video_glitches.txt`.

Phase 2: Database Repair and Analytical Querying
1. Investigate and repair the corrupted index on the `events` table in `/home/user/system.db`.
2. Write a Go program at `/home/user/db_analyze.go` that connects to `system.db` (using `modernc.org/sqlite` or `github.com/mattn/go-sqlite3`).
3. The program must execute a query that uses window functions to calculate the rolling sum of the `impact_score` column for each `service_id` over the last 3 events (ordered by `event_time`).
4. Export the results to `/home/user/rolling_impact.csv` with columns: `service_id`, `event_time`, `rolling_score`.

Phase 3: Query Sanitizer (Adversarial Corpus)
Write a Go module at `/home/user/sanitizer` that builds a CLI tool called `sqlsanitize`.
This tool must accept a file path as an argument, read the file (which contains one SQL query per line), and print ONLY the "clean" queries to standard output. 
It must filter out "evil" queries that contain unauthorized UNION-based injections or attempts to write/drop tables (`DROP`, `DELETE`, `INSERT`, `UPDATE`, `UNION SELECT`). Read-only queries (standard `SELECT` without `UNION`) should be preserved.

The tool will be tested against two hidden corpora: an "evil" corpus and a "clean" corpus. To pass this task, your tool must reject 100% of the queries in the evil corpus and preserve 100% of the queries in the clean corpus.

Ensure all your code is compiled and works properly.
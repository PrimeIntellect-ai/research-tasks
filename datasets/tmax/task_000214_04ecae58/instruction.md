You are assisting a compliance officer in auditing a recent physical security breach using database logs and security footage.

We have a 10-second security video located at `/app/security_cam.mp4` (1 frame per second).
During the breach, the camera feed was hijacked, causing the video frame to turn completely solid red (RGB roughly 255, 0, 0) for exactly one second at the exact moments of unauthorized access. 

You need to:
1. Analyze `/app/security_cam.mp4` to find the exact timestamps (in integer seconds, 0-indexed) where the frame is solid red. (Hint: `ffmpeg` is available).
2. For each detected breach second `T`, calculate the exact epoch timestamp of the breach using the base time of `1730000000`. (i.e., `1730000000 + T`).
3. Query the SQLite database at `/app/compliance.db`. This database contains an `access_logs` table (`id`, `emp_id`, `timestamp`, `resource`) and an `employees` table (`emp_id`, `name`, `manager_id`).
   *IMPORTANT:* The `idx_time` index on the `access_logs` table was corrupted during the system crash. Standard queries filtering on `timestamp` may return stale or missing rows. You MUST bypass or drop this index in your SQL query to retrieve the true records from the table heap for the `MAIN_VAULT` resource at the breach timestamps.
4. For each employee involved in the breach, write a recursive SQL CTE (or Python equivalent) to resolve their full management chain, from the employee themselves all the way up to the CEO (where `manager_id IS NULL`).
5. Create and run a Python HTTP server listening on `127.0.0.1:9090`.
   * It must expose a `GET /breaches` endpoint.
   * It must require an `Authorization: Bearer AUDIT_TOKEN_2024` header. Return `401 Unauthorized` if missing or incorrect.
   * The response must be a JSON array of objects representing the breaches, sorted by `timestamp` descending.
   * Format of the objects: `{"timestamp": 1730000008, "chain": ["Eve", "Frank", "Diana"]}`

Write the necessary Python scripts to perform this analysis and start the server. Leave the server running in the background or foreground so the compliance verifier can query it.
We had a severe incident yesterday in our video processing pipeline, and I need you to triage the aftermath, fix the service, and bring it back online.

Here are your tasks:

1. **Database Recovery**: Our metrics database at `/home/user/incident_data/metrics.db` crashed abruptly. There is uncommitted data in the SQLite WAL file. Recover the database and find the highest `processed_id` from the `jobs` table.
2. **Video Forensics**: Inspect the raw video feed from the incident at `/app/incident.mp4`. The pipeline failed because of a corrupted frame. Find the exact frame number (0-indexed) where the frame is entirely pure red (every pixel is RGB 255, 0, 0).
3. **Git Forensics**: The service requires an administrative API token to start. The developer accidentally committed it to the git repository at `/home/user/service_repo`, but then force-pushed to hide it. Use git history forensics to recover the value of `SECRET_TOKEN`.
4. **Concurrency Debugging**: The Python web service located at `/home/user/service_repo/server.py` has a race condition in its metrics calculation. Multiple threads update a global moving average and variance, leading to numerical instability and incorrect values when hit concurrently. Fix the concurrency issue (e.g., by adding appropriate locks) so the math is stable.
5. **Service Restoration**: Update `server.py` to include a new HTTP GET endpoint at `/api/report`. This endpoint must return a JSON response with the following keys:
   - `"secret_token"`: The recovered secret string.
   - `"red_frame"`: The integer frame index of the red frame from the video.
   - `"recovered_id"`: The integer of the highest `processed_id` you recovered from the database.
   
Start the fixed Python HTTP service so it listens on `0.0.0.0:8000`. Leave it running in the background. Do not require any authentication to access the `/api/report` endpoint.
You are a cloud architect tasked with migrating and optimizing a legacy video analysis service. The system monitors server room feeds, but the old infrastructure is too slow, and network security policies have recently changed, mimicking a scenario where an SSH config silently rejects direct external connections.

We have a 60-second video artefact located at `/app/server_monitor.mp4`.

Currently, there is a legacy, single-threaded Python script at `/home/user/legacy_analyzer.py` that reads this video frame-by-frame and counts the number of "dark frames" (frames where the mean pixel value across all channels is strictly less than 100.0).

Your tasks:
1. **Optimize the Analyzer:** Create a new Python script at `/home/user/fast_analyzer.py` that produces the exact same integer count of dark frames as `legacy_analyzer.py`, but runs significantly faster. You must achieve at least a 3.0x speedup. You may use Python's `multiprocessing`, `concurrent.futures`, or optimized `ffmpeg` subprocess calls to parallelize the frame extraction and analysis. The script must output ONLY the final integer count to stdout.

2. **Network Forwarding:** A local metrics aggregator is listening on `localhost:8080`. Due to simulated security restrictions (where direct connections are blocked), you must create a persistent, background SSH tunnel that forwards local port `9999` to `localhost:8080` via your local user account.

3. **Staged Deployment Script:** Write an idempotent bash script at `/home/user/deploy.sh` that:
   - Ensures the SSH tunnel on port 9999 is running (starting it if it isn't, but not spawning duplicates).
   - Configures a user-level cron job (using `crontab`) that executes `/home/user/fast_analyzer.py` and pipes its output to `nc localhost 9999` every minute. Ensure the crontab update is idempotent (doesn't create duplicate cron entries if run multiple times).

Constraints:
- You do not have `sudo` privileges.
- Your Python script must use standard libraries, `numpy`, `cv2` (OpenCV), or `ffmpeg` binaries. 
- The target output is measured purely by execution time against the legacy baseline.
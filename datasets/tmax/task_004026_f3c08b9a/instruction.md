You are acting as a configuration manager for a legacy data center. We recently experienced a failure in our configuration synchronization service and lost the text-based logs. However, we have a backup video screen recording of the sync activity dashboard, which flashes with different intensities when configuration payloads are processed. 

Your task is to reverse-engineer the configuration change intensity over time from this video and store the metrics in a structured database format.

The video file is located at `/app/sync_dashboard.mp4`.

Perform the following steps entirely using Bash and standard command-line tools (like `ffmpeg`, `ImageMagick`, `awk`, and `sqlite3`):

1. **Frame Extraction & Multi-format Reading**: Extract frames from the video at exactly 1 frame per second (1 FPS). For each extracted frame, calculate its mean grayscale intensity (a float value between 0.0 and 1.0).
2. **Rolling Statistics**: Compute a 5-second rolling moving average of these intensity values. For frame `i` (where `i` starts at 1 for the 1st second), the moving average is the average of the intensities from frame `i-4` up to frame `i`. If fewer than 5 frames exist (e.g., at the start), average whatever is available.
3. **Database Bulk Import**: Format your results into a CSV file with columns: `second`, `intensity`, `moving_avg`. Then, bulk import this CSV into an SQLite database located at `/home/user/config.db` into a table named `sync_history`.
4. **Database Export**: Finally, export the contents of the `sync_history` table as a JSON array of objects to `/home/user/rolling_stats.json`.

Ensure your calculations are accurate and properly outputted to the JSON file. We will verify your exported JSON file programmatically by comparing the moving average numbers against our internal reference.
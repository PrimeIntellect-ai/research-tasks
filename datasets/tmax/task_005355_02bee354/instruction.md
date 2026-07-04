You are an operations data analyst working with presentation assets and metadata. You have a multi-stage data processing pipeline to set up on your system.

Your environment contains:
- A video file with embedded subtitles at `/app/presentation.mp4`.
- A CSV file containing user engagement events at `/app/metadata.csv` with columns: `timestamp,event_type,user_comment` (timestamps are in ISO 8601 format, e.g., `2023-10-15T14:25:01Z`).

Please complete the following tasks:

1. **Feature Extraction (Video/Text):**
   Extract the primary subtitle stream from `/app/presentation.mp4` and save it as an SRT file to `/home/user/subs.srt`. Use `ffmpeg`.

2. **Time-based Bucketing:**
   Process `/app/metadata.csv`. Count the total number of events bucketed by the hour. Write the output to `/home/user/hourly_counts.txt` in the format `YYYY-MM-DD HH:00,count` (e.g., `2023-10-15 14:00,42`), sorted chronologically.

3. **Similarity Computation:**
   Write a standalone, executable Bash script at `/home/user/metric.sh` that takes exactly two string arguments and computes their Token Jaccard Similarity index. 
   
   The script must follow these exact rules:
   - Convert both input strings to lowercase.
   - Replace all non-alphanumeric characters (anything other than `a-z` and `0-9`) with spaces.
   - Split each string into a set of unique words (ignoring empty strings).
   - Compute the size of the Intersection of the two sets (words present in both sets).
   - Compute the size of the Union of the two sets (total unique words across both sets combined).
   - If the Union size is 0 (i.e., neither string contained any alphanumeric words), output exactly `1000`.
   - Otherwise, output the integer result of `(Intersection * 1000) / Union` (using standard integer division, discarding any remainder).
   - The script must print only this integer to standard output and exit. It must be written primarily in Bash (using standard coreutils like `tr`, `sed`, `grep`, `sort`, `awk` etc. is expected).

4. **Pipeline Scheduling:**
   Create a dummy shell script at `/home/user/cleanup.sh` that simply contains `#!/bin/bash` and `echo "cleaned"`. Ensure it is executable. Install a cron job for the current user that executes `/home/user/cleanup.sh` every day at exactly 02:30 AM.

Ensure all file paths match exactly and `/home/user/metric.sh` handles edge cases like empty strings or strings with only punctuation correctly.
You are acting as a Data Analyst. We receive a daily CSV file containing customer feedback, and we need an automated Bash pipeline to process it, normalize the text, extract the top keywords, and generate a daily report. 

Please perform the following tasks:

1. **Create a processing script** at `/home/user/process.sh` that does the following:
   - Reads the CSV file located at `/home/user/data/feedback.csv`. The file has headers: `id,username,feedback_text`.
   - Streams the `feedback_text` column (3rd column). Note that the text might contain commas inside quotes (standard CSV). To keep it simple, assume you can use a basic CSV parser or `awk -F','` if you strip quotes, but wait, the setup ensures the 3rd column is simply the last column and doesn't contain internal commas for this specific system. Let's assume the delimiter is strictly a pipe `|` to avoid CSV parsing complexities in bash. The file is at `/home/user/data/feedback.csv` with headers `id|username|feedback_text`.
   - Normalizes the `feedback_text`: converts all text to lowercase, replaces all non-alphabetic characters (anything not `a-z`) with spaces, and splits the text into individual words (tokenization).
   - Filters out any words that are less than 4 characters long.
   - Calculates the top 3 most frequent valid words and their occurrence counts.
   - Reads the template file at `/home/user/template.txt` and replaces the exact placeholders `{{WORD1}}`, `{{COUNT1}}`, `{{WORD2}}`, `{{COUNT2}}`, `{{WORD3}}`, and `{{COUNT3}}` with the top 3 words and their counts (Rank 1 being the most frequent).
   - Saves the filled template to `/home/user/reports/summary.txt`.
   - Appends a log entry to `/home/user/logs/pipeline.log` in the exact format: `[YYYY-MM-DD HH:MM:SS] Pipeline completed successfully.` using the current system time.

2. **Execute the script** once manually so that `/home/user/reports/summary.txt` and `/home/user/logs/pipeline.log` are generated.

3. **Schedule the script** to run automatically via `cron`. Install a crontab for the `user` that runs `/home/user/process.sh` exactly at 2:00 AM server time every day.

Constraints & Details:
- The script must be written in Bash (`#!/bin/bash`).
- Create any missing output directories (`/home/user/reports/`, `/home/user/logs/`).
- Do not use Python, Perl, or Ruby; rely on standard Unix tools (e.g., `awk`, `sed`, `tr`, `sort`, `uniq`, `grep`).
- If there is a tie in word frequency, sort them alphabetically.
- Make sure the script is executable.
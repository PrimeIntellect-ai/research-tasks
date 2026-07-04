You are tasked with building a data processing pipeline for our configuration management system. We recently experienced issues with obfuscated configurations and need to track changes accurately.

Part 1: Video Analysis
We have a screen recording of our monitoring dashboard at `/app/server_monitor.mp4`. The dashboard turns red when a critical configuration change is detected. 
Using `ffmpeg` and any image processing tools (like ImageMagick), extract the frames at 1 frame per second. Count the number of frames where the average color of the frame is predominantly red (the red channel average is significantly higher than green and blue, e.g., R > 150, G < 50, B < 50).
Write the final integer count of these "red alert" frames to `/home/user/red_alert_count.txt`.

Part 2: Configuration Sanitizer
We need a robust Bash script at `/home/user/validate_configs.sh` that acts as a filter for new configuration files.
The script must take a single file path as an argument:
`bash /home/user/validate_configs.sh <path_to_config_file>`

The script must:
1. Parse the file, expecting `KEY=VALUE` pairs (one per line).
2. Reject the file (exit with status 1) if it contains duplicate keys (hash-based deduplication logic).
3. Reject the file (exit with status 1) if it contains hidden malicious Unicode characters, specifically Zero-Width Spaces (U+200B) or Bidirectional Override characters (U+202E, U+202D).
4. Reject the file (exit with status 1) if the values do not match standard alphanumeric characters, basic punctuation, or valid multi-language text (no executable shell metacharacters like backticks or unescaped `$()`).
5. Accept the file (exit with status 0) if it passes all checks.
6. Append a log entry to `/home/user/pipeline.log` for every file processed, in the format: `[TIMESTAMP] FILE=<filename> STATUS=<ACCEPTED|REJECTED>`

Ensure your script is efficient and correctly handles edge cases. We will run your script against a hidden dataset of clean and malicious configuration files.
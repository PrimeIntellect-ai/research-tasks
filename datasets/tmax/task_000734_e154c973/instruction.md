You are an incident response log analyst investigating a series of sophisticated bypasses in our monitoring pipeline. Our previous pipeline was a naive script that silently dropped CSV rows containing embedded newlines, allowing attackers to hide malicious payloads. 

We recovered an audio dictation from the senior engineer who first spotted the anomaly before they went on leave. The audio is located at `/app/incident_dictation.wav`. It contains critical parameters for the new detection logic.

Your task is to build a robust C-based log detector that implements the exact mathematical and temporal rules specified in the audio recording.

Requirements:
1. Listen to / transcribe the audio file at `/app/incident_dictation.wav` to discover the exact detection parameters (a specific time-bucketing threshold and a string distance anomaly target).
2. Write a C program, compiled to an executable located at `/home/user/log_detector`.
3. The executable must take exactly one argument: the path to a CSV log file.
    * Usage: `/home/user/log_detector <path_to_csv>`
4. The CSV files have the following columns: `timestamp,user_id,message`
    * `timestamp`: ISO 8601 format (e.g., `2023-10-25T14:30:00Z`).
    * `user_id`: An alphanumeric string.
    * `message`: A multi-language UTF-8 string enclosed in double quotes. It MAY contain embedded newlines, which your parser must handle correctly (do not silently drop or truncate these rows).
5. The program must evaluate the CSV file against the rules dictated in the audio:
    * It must group logs into time buckets based on the specified duration.
    * It must calculate the character-level similarity (Levenshtein distance on UTF-8 codepoints) between the `message` field and the restricted keyword mentioned in the audio.
6. The program must return exit code `1` (reject/flag) if the CSV file violates ANY of the rules specified in the audio (either the time-bucketing threshold is exceeded, or a message is mathematically too close to the restricted keyword).
7. The program must return exit code `0` (accept/clean) if the file perfectly adheres to the rules.

You may use standard Linux terminal tools (Python, ffmpeg, etc.) to analyze the audio and prepare your environment, but the final detector MUST be written in C. Make sure you handle multi-byte Unicode characters properly when calculating the string distance.
You are an ETL log analyst investigating a pipeline that produces duplicate records upon job retries.

First, you need to recover the specific log parsing rules. The engineering team encoded the log regex pattern into a video file located at `/app/pattern_source.mp4`. 
To recover the regex pattern:
1. Extract every frame of the video.
2. Calculate the average grayscale pixel intensity for each frame (rounded to the nearest integer).
3. Convert these integers into ASCII characters.
4. Concatenate the characters in frame order to reveal the regex string. The regex will contain named capture groups `job` and `data`.

Next, write a Python 3 script at `/home/user/process_logs.py` that implements the deduplication filter. The script must:
1. Read log lines from standard input (stdin).
2. Match each line against the regex pattern recovered from the video. Lines that do not match should be silently ignored.
3. For matching lines, extract the `job` and `data` strings.
4. Normalize the `data` string by:
   - Converting it to strictly lowercase.
   - Replacing any sequence of two or more whitespace characters with a single space character.
   - Stripping any leading or trailing whitespace.
5. Compute the MD5 hash (hexadecimal string) of the normalized `data`.
6. Maintain a record of hashes seen per `job`. If the MD5 hash has already been processed for that specific `job` ID, treat the line as a duplicate retry and drop it.
7. For new (non-duplicate) records, print to standard output (stdout) a single line formatted exactly as:
   `{job}\t{normalized_data}\t{md5_hash}`

Ensure your script is executable (`chmod +x /home/user/process_logs.py`) and includes a shebang `#!/usr/bin/env python3`. Your script will be aggressively tested against a massive stream of fuzzed logs to ensure its behavior is bit-exact with the reference implementation. Do not print any extraneous debug information to stdout.
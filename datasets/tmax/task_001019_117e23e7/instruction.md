You are tasked with building a configuration log sanitizer for our change-tracking system. We have been receiving corrupted JSON-lines logs that contain malformed unicode escape sequences, as well as adversarial log floods from specific users.

Your goal is to write a Python script at `/home/user/sanitizer.py` that acts as a strict detector. The script will take a single argument, the path to a JSON-lines log file, and analyze it line by line. 

The script must exit with code `0` if the log file is perfectly "clean", and exit with code `1` if it contains ANY "evil" lines.

An "evil" log file contains one or more lines meeting ANY of the following criteria:
1. **Malformed Unicode:** The raw JSON string contains an invalid unicode escape sequence (i.e., `\u` followed by anything other than exactly 4 hexadecimal digits). You must detect this before or during parsing.
2. **Rate Limit Exceeded:** A single `user_id` performs more than `N` configuration changes within any rolling window of `M` seconds. The log lines contain a `timestamp` field (Unix epoch seconds) and a `user_id` string.

**Finding N and M:**
The values for N and M are hidden in a system diagnostic video located at `/app/status_flashes.mp4`. 
- `N` is the exact number of frames in the video that are purely, entirely red (RGB: 255, 0, 0).
- `M` is the exact number of frames in the video that are purely, entirely green (RGB: 0, 255, 0).
You must extract the frames and count these specific colors to find your rate-limiting parameters.

Your script will be tested against two corpora of logs:
- A directory of clean logs that must all return exit code `0`.
- A directory of evil logs that must all return exit code `1`.

Your script should be robust, well-structured, and capable of handling varying timestamps and user activities.
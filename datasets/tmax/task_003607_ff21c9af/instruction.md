It is 3:00 AM, and you have just been paged. The critical SecureCam video analytics pipeline has crashed, and the incident response team needs you to restore the core query processing function immediately. 

Here is what we know about the incident:
1. **Video Artefact**: The processing crashed while analyzing `/app/incident_feed.mp4`. The video contains a flashing diagnostic LED in the top-left corner (a 10x10 pixel block). You need to extract the 32-bit hexadecimal key transmitted by this LED. A bright frame is a `1` bit, and a dark frame is a `0` bit. Read the bits sequentially from frame 0 to frame 31 to form a 32-bit integer, then format it as a zero-padded 8-character hex string.

2. **Memory Dump Analysis**: The crashed process dumped its memory at `/app/coredump.raw`. The process environment contained a critical 16-character alphanumeric `QUERY_SALT` string right before the crash. You must extract this salt from the dump. It is prefixed in memory by the string `SALT_START=` and ends with `_SALT_END`.

3. **Git Forensics & Delta Debugging**: The source code for the query logic is in the Git repository at `/app/query_service`. A recent commit broke the `compute_query.py` script. The script takes an integer input, combines it with the secret key and salt, and performs a hashing routine. 

Your objective is to write a fixed, standalone Python script at `/home/user/fixed_query.py`. 
The script must:
- Accept exactly one integer as a command-line argument.
- Use the 8-character hex key extracted from the video.
- Use the 16-character salt extracted from the memory dump.
- Perform the hashing routine exactly as intended in the pre-bug commit (you will need to investigate the git history to find the correct logic).
- Print ONLY the final integer output to `stdout`.

We will verify your script by fuzzing it with thousands of random integers against a secure, stripped oracle binary that implements the correct logic. Ensure your output perfectly matches the reference logic for all 32-bit unsigned integer inputs.
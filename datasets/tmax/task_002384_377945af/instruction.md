A customer has reported a severe regression in our video telemetry processing pipeline, and I need you to act as our support engineer to collect diagnostics and provide an immediate workaround. We have a git repository at `/home/user/telemetry_pipeline` which contains the pipeline code, including a custom binary utility `telemetry_encoder` built from C source.

Recently, three things happened:
1. The `telemetry_encoder` started outputting corrupted data.
2. The customer reported that our video telemetry is failing on a specific video. We have secured the diagnostic video at `/app/diagnostic_clip.mp4`. You will need to extract the frames using `ffmpeg` to verify the pipeline's behavior on this specific clip.
3. The customer's security team suspects a diagnostic API key was accidentally committed to the git repository and later removed, but remains in the history.

Your task is to:
1. **Git History Forensics:** Search the git history of `/home/user/telemetry_pipeline` to find the leaked API key (it was assigned to a variable named `DIAGNOSTIC_API_KEY`). Save exactly this key (and nothing else) to `/home/user/leaked_key.txt`.
2. **Git Bisection:** Use git bisection to identify the exact commit hash that introduced the bug in the `telemetry_encoder`. The bug causes the encoder to fail when processing coordinates from the video. Save the full 40-character commit hash to `/home/user/broken_commit.txt`.
3. **Binary Replacement:** Because the C compiler on our production system is currently broken, we cannot just revert the commit and recompile. You must reverse-engineer the correct behavior of the *working* `telemetry_encoder` binary (from before the regression) and implement a bit-exact equivalent in Python. 
   - Write this to `/home/user/encoder_fix.py`.
   - Your Python script must accept a single integer argument (the telemetry coordinate) and print the encoded hexadecimal string to standard output, exactly matching the behavior of the pre-regression binary. 

Ensure your final Python script perfectly matches the logic of the working binary, as it will be rigorously verified against millions of possible inputs.
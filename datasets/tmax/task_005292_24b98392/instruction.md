You are tasked with investigating a critical memory leak in a long-running video processing service written in Bash. The service processes surveillance feeds, extracts metadata, and updates a local database. Recently, it has been crashing with out-of-memory (OOM) errors. 

Here is what we know:
1. **The Crash:** The service crashed while processing `/app/surveillance_feed.mp4`. 
2. **Corrupted State:** The crash corrupted the local database journal (`/home/user/service/state.wal`). You must parse this custom WAL (Write-Ahead Log) to recover the last successfully processed frame index before the crash. The WAL consists of hexadecimal block entries; valid entries start with `0xAA` and end with `0xBB`, containing the frame number as a 32-bit hex float that suffered a floating-point precision error during logging. You'll need to repair the float precision to map it back to an integer frame number, finding the exact frame the service died on.
3. **The Root Cause:** We suspect the OOM is caused by malformed metadata associated with certain frames triggering an infinite recursion or unterminated loop in the service's metadata parser.
4. **The Fix:** We need you to write a Bash-based metadata sanitizer script at `/home/user/sanitizer.sh`. This script will receive metadata payloads via `stdin` and must output the sanitized payload to `stdout`, or exit with code 1 if the payload is irreparably malicious (causing the infinite loop). 

Your objectives:
1. Extract the frames of `/app/surveillance_feed.mp4` using `ffmpeg` to investigate the video visually around the crash point.
2. Recover the last successful frame index from `/home/user/service/state.wal`. Output this single integer to `/home/user/crash_frame.txt`.
3. Develop the Bash filter `/home/user/sanitizer.sh`. We have provided samples of normal metadata in `/home/user/metadata/clean/` and malicious metadata (which causes the recursion/memory leak) in `/home/user/metadata/evil/`. 
4. Your `sanitizer.sh` must successfully `exit 0` and pass through the payload for clean data, and `exit 1` for evil data.

Ensure `/home/user/sanitizer.sh` is executable and operates exclusively using Bash and standard coreutils.
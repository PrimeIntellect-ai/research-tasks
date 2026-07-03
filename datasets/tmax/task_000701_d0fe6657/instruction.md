You are tasked with debugging a failing build system for a project. The build system is written in Bash and consists of multiple scripts. Recently, the build started hanging and eventually failing due to a timeout. 

Here is what you need to do:

1. **Fix the Infinite Recursion:** 
   The main build script runs `/home/user/project/scripts/resolve_deps.sh`, which is supposed to parse `/home/user/project/deps.txt` and recursively resolve dependencies, outputting them to `/home/user/project/resolved.txt`. However, a cyclic dependency was recently introduced in `deps.txt`, causing `resolve_deps.sh` to get stuck in an infinite recursive loop.
   You need to modify `/home/user/project/scripts/resolve_deps.sh` to handle cyclic dependencies. A dependency should only be processed and added to `resolved.txt` once. If it has already been visited or resolved, it should be skipped. 
   Once fixed, run `/home/user/project/build.sh`. Ensure `/home/user/project/resolved.txt` contains the correct list of uniquely resolved dependencies.

2. **Statistical Anomaly Investigation:**
   The developers noticed intermittent slowdowns before the infinite loop issue. Look at `/home/user/project/logs/download.log`. Each line logs the download time of a dependency. Find the single dependency that took more than 5000ms to download. Write the exact name of this dependency to `/home/user/anomaly.txt`.

3. **Log Timeline Reconstruction:**
   The build system uses multiple workers, which log to different files in `/home/user/project/logs/` (e.g., `worker1.log`, `worker2.log`, `download.log`). 
   Combine all the logs from the `/home/user/project/logs/` directory into a single file at `/home/user/timeline.txt`. The combined log file must be sorted chronologically by the timestamp in the log lines. The expected format for the timeline file is the exact lines from the original log files, just sorted by the `[YYYY-MM-DDTHH:MM:SS]` timestamp at the beginning of each line.

Ensure that all requested output files (`resolved.txt`, `anomaly.txt`, `timeline.txt`) exist in their specified locations and contain the correct, strictly formatted data.
You are a Site Reliability Engineer (SRE) investigating an issue with your team's custom uptime monitoring daemon. The daemon, written in C++, reads a dependency graph of microservices and recursively checks their health. Recently, a configuration update caused the monitor to crash with a segmentation fault (stack overflow) due to an infinite recursion bug when processing cyclic dependencies.

Your task is to perform root cause analysis, fix the code, and establish a regression test. 

All files are located in `/home/user/uptime_monitor`.

**Phase 1: Delta Debugging (Test Minimization)**
The failing configuration is at `/home/user/uptime_monitor/services.txt`. It contains hundreds of dependency declarations in the format `ServiceA ServiceB` (meaning ServiceA depends on ServiceB). 
1. Isolate the exact minimal subset of lines from `services.txt` that triggers the crash in the compiled `monitor` binary.
2. Save this minimized configuration to `/home/user/uptime_monitor/minimal_crash.txt`. It must contain ONLY the lines that form the cyclic dependency causing the infinite recursion.

**Phase 2: Fix the Recursion Bug**
The source code is at `/home/user/uptime_monitor/monitor.cpp`.
1. Modify `monitor.cpp` to properly track visited nodes during its recursive dependency check.
2. If a cyclic dependency is detected during recursion, the program should immediately stop recursing that path, print `CYCLE DETECTED: <ServiceName>` to standard output, and continue processing remaining nodes cleanly without crashing.
3. The program must exit with a status code of `0` when it successfully completes, even if cycles were found.

**Phase 3: Regression Testing**
1. Write a bash script at `/home/user/uptime_monitor/regression_test.sh` that:
   - Compiles `monitor.cpp` into an executable named `monitor` using `g++` (e.g., `g++ -O2 monitor.cpp -o monitor`).
   - Runs the compiled `monitor` binary using your `/home/user/uptime_monitor/minimal_crash.txt` file as input.
   - Redirects the standard output of the execution to `/home/user/uptime_monitor/test_result.log`.
2. Ensure the script is executable (`chmod +x`).

**Success Criteria:**
- `minimal_crash.txt` contains exactly the lines forming the cycle.
- `monitor.cpp` is fixed and no longer segfaults.
- Executing `/home/user/uptime_monitor/regression_test.sh` produces a `test_result.log` containing the "CYCLE DETECTED" message and returns an exit code of 0.
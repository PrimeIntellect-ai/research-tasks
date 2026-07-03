You are acting as a Site Reliability Engineer (SRE). Our internal C-based uptime monitoring service recently crashed, generating a memory dump. There are several issues you need to resolve to get the service back online and accurate.

Your tasks are:
1. **Memory Dump Analysis**: We saved a partial memory dump of the crashed process at `/home/user/uptime_project/memory.dmp`. Extract the hostname of the server it was processing when it crashed. The hostname is stored in the memory dump immediately following the string `SLA_TARGET_HOST=`. Save ONLY the hostname to `/home/user/crashing_host.txt`.
2. **Dependency Conflict Resolution**: The project Makefile in `/home/user/uptime_project/Makefile` is currently pointing to a legacy header directory (`./legacy_headers`) which contains outdated definitions causing buffer overflows. Change it to use the modern headers directory (`./modern_headers`).
3. **Formula Correction**: The SLA percentage calculation in `/home/user/uptime_project/src/uptime_monitor.c` is currently outputting `0.00` for valid uptimes due to a standard C arithmetic bug (integer division). Fix the formula in the `calculate_sla` function so it correctly calculates a floating-point percentage.
4. **Recompile**: Run `make` in `/home/user/uptime_project` to build the fixed binary. The resulting binary should be located at `/home/user/uptime_project/uptime_monitor`.

Ensure all file paths and modified code are exact. Do not change the function signatures or overall architecture, just fix the bugs and build.
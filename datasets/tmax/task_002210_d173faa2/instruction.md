Wake up, engineer! It's 3:00 AM and you've just been paged. The production telemetry ingestion service went down right after the midnight release. The previous on-call engineer tried to rollback, but now the codebase won't even compile, and incoming sensor data is backing up.

Your workspace is located at `/home/user/telemetry_svc/`. The service processes raw sensor logs and outputs a cleaned CSV. 

There are three distinct issues you must identify and fix:
1. **Compilation/Linker Failure:** The project currently fails to build. Fix the build configuration or source code so that running `make` in `/home/user/telemetry_svc/` successfully compiles the `parser_svc` binary.
2. **Crash on Edge Case:** Once built, if you run `./parser_svc /home/user/sensor_data.csv /home/user/clean_data.csv`, it crashes. Analyze the logs or use a debugger to find the format parsing edge case causing the segfault, and patch the C code.
3. **Precision Loss:** Downstream services are reporting that the timestamps in the output data are corrupted (losing microsecond precision). Identify where the precision loss is occurring in the C code and fix it so the exact microsecond timestamps are preserved.

**Requirements:**
- Fix the code and `Makefile` in `/home/user/telemetry_svc/`.
- Run the fixed binary: `./parser_svc /home/user/sensor_data.csv /home/user/clean_data.csv`
- The output file `/home/user/clean_data.csv` must contain the correctly parsed data with intact high-precision timestamps.
- Write a brief post-mortem to `/home/user/postmortem.txt` detailing the three bugs (linker missing flag, the format parser null dereference, and the variable type causing precision loss).

Do not change the command line arguments of the binary or the overall architecture. Just fix the bugs so the system can recover.
You are an SRE investigating a severe memory leak in our real-time log processing pipeline. The pipeline ingests timestamped events, normalizes their timezones to UTC, and stores the aggregated metrics in Redis. Recently, malformed timezone payloads have been causing the C++ processing service to leak memory and eventually crash.

The system is composed of three services:
1. A Redis instance (stores metrics).
2. The C++ Log Processor (listens on TCP port 8080).
3. A Log Generator (simulates incoming traffic).

Your task has two parts:

**Part 1: Service Debugging and Fixing**
1. Review the C++ source code for the log processor located in `/home/user/src/log_processor.cpp`. 
2. Use tools like `valgrind`, `strace`, or `gdb` to identify the memory leak. The leak occurs when the service processes edge-case timezone offsets (e.g., offsets with invalid minutes or bounds). Additionally, there is a formula error in how offsets are applied to the UNIX timestamp.
3. Fix the memory leak and the formula bug in `/home/user/src/log_processor.cpp`.
4. Recompile the service: `g++ -O2 -std=c++17 /home/user/src/log_processor.cpp -o /home/user/bin/log_processor -lhiredis -lpthread`
5. Ensure the end-to-end pipeline functions correctly. You can start all services by running `/app/start_services.sh`. 

**Part 2: Adversarial Corpus Sanitizer**
To prevent future regressions, the security team requires a standalone C++ CLI tool that acts as a pre-filter for logs.
1. Create a C++ program at `/home/user/src/detector.cpp` and compile it to `/home/user/bin/detector`.
2. The detector must read a single JSON log line from standard input.
3. If the log contains a mathematically valid timezone offset (between -12:00 and +14:00, with minutes between 00 and 59), the program MUST exit with code `0`.
4. If the log contains a malformed or out-of-bounds timezone offset (which triggers the leak/bug), the program MUST exit with code `1`.

Your solution will be tested against two corpora of logs:
- A "clean" corpus of valid logs.
- An "evil" corpus of logs containing the malicious timezone strings that trigger the memory leaks.

Ensure your `detector` correctly classifies 100% of both corpora.
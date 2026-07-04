You are a site reliability engineer investigating a severe memory leak in a long-running telemetry aggregation service. The service is written in C and runs on a local Linux server. It ingests binary log payloads from various simulated microservices.

Recently, the service has been experiencing memory exhaustion. You suspect that a specific malformed log payload is triggering a format parsing edge-case, resulting in a memory leak.

Your environment is set up as follows:
- `/home/user/telemetryd/`: Contains the source code (`server.c`, `parser.h`), a `Makefile`, and a client test script (`test_runner.sh`).
- `/home/user/logs/`: Contains 100 binary log files (`log_000.bin` to `log_099.bin`) captured from the network.

Your tasks:
1. **Fix the Build:** The project currently fails to compile due to missing compiler flags and a minor header issue. Diagnose and fix the build failures so `make` successfully produces the `telemetryd` executable.
2. **Reproduce and Isolate:** Run the service and use the `test_runner.sh` script to replay the logs. Identify the *exact single log file* that causes the memory leak. You may want to use tools like `valgrind` and delta debugging techniques to isolate the faulty payload.
3. **Analyze the Root Cause:** The binary payload uses a simple Length-Value format. Find the edge case in `server.c` where a format parsing error leads to an un-freed memory allocation.
4. **Patch the Service:** Modify `server.c` to fix the memory leak. Ensure the service still correctly processes valid records and cleanly rejects/breaks on invalid ones without leaking memory.
5. **Report:** Create a file at `/home/user/report.txt` with the following exact format:
   ```
   Faulty Log: log_XXX.bin
   Leaked Bytes per request: Y
   ```
   *(Where `log_XXX.bin` is the name of the file causing the leak, and `Y` is the exact number of bytes leaked during a single processing of that specific faulty log before your patch).*

Ensure your fixed `telemetryd` compiles and runs cleanly without memory leaks when processing all 100 logs.
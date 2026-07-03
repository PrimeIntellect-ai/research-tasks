You are an Site Reliability Engineer debugging an internal uptime monitoring agent. The tool, `uptime-analyzer`, is written in C and parses JSON telemetry payloads to calculate service availability percentages. 

Currently, the tool cannot even build due to linker and compiler errors originating from our vendored dependencies, and we suspect the uptime formula implementation has a critical bug that needs correction once compiled.

Your objectives:
1. **Fix the Vendored Dependency Build:** We vendor `cJSON` (a C JSON parser) at `/app/cJSON-1.7.15`. When you try to build it using its `Makefile`, the creation of the static archive fails due to a typo in the archive command. Diagnose and fix the compiler/linker step so `libcjson.a` builds correctly.
2. **Build the Analyzer:** Navigate to `/app/uptime-analyzer`. Its Makefile expects `libcjson.a` to be available. Build the `analyzer` binary successfully.
3. **Correct the Uptime Formula:** The binary accepts a JSON string as an argument, for example: `{"server": "db-prod", "pings": 5000, "missed": 34}`. 
   It is supposed to calculate and print the uptime percentage formatted exactly as: `Server db-prod: 99.32%` (always to two decimal places).
   However, the current C implementation in `analyzer.c` incorrectly calculates the percentage, often outputting `0.00%` or `100.00%` due to a data type or formula bug. Analyze the diff between the expected mathematical logic and the current implementation, and fix `analyzer.c`.
4. **Final Integration:** Compile the fixed version and place the final executable at `/home/user/uptime-analyzer-fixed`.

Ensure the final executable accurately processes any valid JSON payload in that format and handles the calculation accurately. The automated verifier will pass thousands of randomly generated JSON strings to your binary to ensure its output is bit-exact equivalent to our reference monitoring logic.
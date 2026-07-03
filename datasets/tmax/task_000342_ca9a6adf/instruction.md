You are an engineer investigating a persistent memory leak in a long-running C++ data processing service. The service parses floating-point sensor readings from standard input, normalizes them, and performs some analytics. 

However, the service frequently crashes with Out-Of-Memory (OOM) errors. The crashes seem to occur when the service receives "dirty" data—either completely corrupted strings or specific edge-case floating-point values that cause precision errors, division-by-zero, `NaN`, or `Infinity` results.

You have been provided the source code of the buggy service at `/home/user/sensor_service.cpp`.

Your tasks are to:
1. **Analyze the Code**: Identify the memory leaks caused by corrupted input exceptions and floating-point anomalies.
2. **Create Minimal Reproducible Examples (MREs)**: 
   - Create a file `/home/user/mre_math.txt` containing exactly one line of input (a number) that triggers the `NaN` or `Infinity` floating-point math leak.
   - Create a file `/home/user/mre_corrupt.txt` containing exactly one line of input (non-numeric text) that triggers the unparseable exception memory leak.
3. **Fix the Service**: Create a repaired version of the code at `/home/user/fixed_service.cpp`. Your fix must:
   - Gracefully catch parsing exceptions without leaking memory.
   - Prevent division-by-zero or precision-based `Inf`/`NaN` vulnerabilities by adding a precision check (e.g., if the reading is within `1e-9` of the problematic denominator, reject it gracefully without leaking).
   - Prevent any memory leaks from occurring regardless of the input.
4. **Compile**: Compile your fixed code using `g++ -O2 /home/user/fixed_service.cpp -o /home/user/fixed_service`.

To succeed, `/home/user/fixed_service` must process both of your MRE files (and a hidden test file with millions of mixed valid/corrupted lines) cleanly, with Valgrind reporting absolutely 0 bytes leaked. Do not change the standard normal output format for valid values.
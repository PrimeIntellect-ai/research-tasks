You are a performance engineer tasked with debugging and profiling a financial analytics application that has been producing incorrect results and causing numerical overflows.

You have been given a workspace at `/home/user/app` with the following files:
1. `analyzer.cpp` - A C++ program that calculates the Exponential Moving Average (EMA).
2. `memory.bin` - A partial memory dump from a recent crash.

Your tasks are:
1. **Memory Dump Analysis**: Analyze `/home/user/app/memory.bin`. Somewhere in this binary blob is a configuration key starting with `TEST_KEY_` followed by exactly 6 digits (e.g., `TEST_KEY_123456`). Extract this key and save it to a new file at `/home/user/app/key.txt` (the file should contain only the key, with no other text).
2. **Formula Implementation Correction**: Inspect `/home/user/app/analyzer.cpp`. The `calculate_ema` function contains a mathematical bug in the EMA formula. The weighting multiplier for the previous EMA value is incorrectly implemented as `(1.0 + k)`. Fix the formula in the code so it correctly uses `(1.0 - k)`.
3. **Regression Test Construction**: Create an executable bash script at `/home/user/app/test.sh`. This script must:
   - Compile `analyzer.cpp` into an executable named `analyzer` using `g++`.
   - Run the compiled `./analyzer` program.
   - Capture the output. The corrected program with the default values should output `EMA: 11.5556`. 
   - If the output matches `EMA: 11.5556`, the script must exit with status code 0. If it does not match or fails to compile, it must exit with status code 1.

Ensure `/home/user/app/test.sh` has executable permissions.
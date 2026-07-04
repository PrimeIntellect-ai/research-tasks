We have a long-running mathematical evaluation service that has been crashing repeatedly due to a severe memory leak, and it occasionally dumps core when encountering edge cases in our custom input format. The original source code was lost during a recent migration, and the build pipeline is currently failing, preventing us from restoring it.

All we have is a stripped binary of the last working version located at `/app/calc_service_stripped`. 

Your task is to:
1. Analyze the binary `/app/calc_service_stripped` (and its behavior) to deduce the mathematical formula it computes. It reads a custom string format from standard input, parses it, and outputs an integer.
2. The binary expects inputs in a specific delimited prefix format: `OP[arg1,arg2]`, where `OP` is an operation code (like `SEQ` for our proprietary sequence) and arguments are integers. 
3. Figure out how the mathematical sequence is generated. 
4. Implement a memory-safe, identical replacement in Python. Your script must be saved to `/home/user/clean_calc.py`.
5. Your script must accept a single command-line argument representing the input string, parse it robustly (handling the edge cases that crashed the C++ version, such as negative numbers or missing brackets, by printing "INVALID_FORMAT"), and print the exact same numerical result as the binary would for valid inputs.

Our automated testing suite will fuzz-test your `/home/user/clean_calc.py` script against the original `/app/calc_service_stripped` using 10,000 random valid inputs to ensure bit-exact output equivalence.
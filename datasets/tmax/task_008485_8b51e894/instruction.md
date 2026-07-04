You are a developer transitioning a legacy Python utility to a high-performance C program. The utility parses server access logs, decodes hex-encoded requested URIs, identifies users (IPs) that are hitting restricted endpoints (`/api/v1/`), and flags IPs that exceed a rate limit threshold (more than 2 requests).

In `/home/user/util_dev/`, you have two files:
1. `legacy_parser.py`: The reference implementation. It reads `stdin`, filters and decodes, and outputs rate-limit violators.
2. `fast_parser.c`: The drafted C implementation. It compiles, but produces incorrect output for certain logs.

Your task:
1. **Debug and fix** `fast_parser.c`. There is a logic flaw in how it handles data encoding and/or parsing compared to the Python script. You must translate the exact behavior of `legacy_parser.py` into the C code.
2. **Write a test script** at `/home/user/util_dev/test_runner.sh`. This bash script must:
   - Compile `fast_parser.c` using `gcc -o fast_parser fast_parser.c`.
   - Generate a mock log file at `/home/user/util_dev/test_log.txt` containing at least 8 log lines. The mock data must include cases that trigger the rate limit and expose the original bug in the C code (e.g., varying cases in hex encoding).
   - Run both `legacy_parser.py` and `./fast_parser` on `test_log.txt`.
   - Sort the outputs of both programs, save them to `py_out.txt` and `c_out.txt` respectively, and compare them using `diff`.
   - Write the output of the `diff` command to `/home/user/util_dev/diff_output.txt`.
   - Exit with code 0 if the diff is empty (successful test), or >0 if there are differences.

Log format (space-separated):
`[TIMESTAMP] [IP_ADDRESS] [HEX_ENCODED_URI]`
Example: `1610000000 192.168.1.1 2f6170692f76312f64617461` (which decodes to `/api/v1/data`)

Output format of the parsers:
`[IP_ADDRESS] [VIOLATION_COUNT]`

Ensure `/home/user/util_dev/diff_output.txt` is exactly empty after running your `test_runner.sh`, indicating 100% parity between the fixed C code and the legacy Python script.
You are tasked with developing a robust, high-performance C utility for filtering streaming log data based on rate limits, and then writing a property-based test to verify its correctness.

Your objective is to create a C program, a build script, and a testing script.

### 1. The C Utility (`/home/user/rate_filter.c`)
Write a C program that reads log lines from standard input (stdin) and prints valid, non-rate-limited lines to standard output (stdout). 
* **Input Format:** Each line will be formatted exactly as `<timestamp> <IP_ADDRESS> <message>`, where:
  * `<timestamp>` is a positive integer (Unix epoch seconds). Note: The input stream is guaranteed to have non-decreasing timestamps (chronological order).
  * `<IP_ADDRESS>` is an IPv4 address (e.g., `192.168.1.1`).
  * `<message>` is an arbitrary string containing no newlines.
* **Rate Limiting Rule:** An IP address is allowed a maximum of `MAX_REQ` requests per second (i.e., per unique timestamp). If an IP exceeds this limit for a specific timestamp, the excess log lines for that IP and timestamp should be dropped (not printed).
* **Custom Data Structure:** You must implement a custom hash map or linked-list based tracking structure in C to keep track of IP hit counts for the current timestamp. Do not use external libraries (like GLib) for this data structure. When the timestamp changes, you should clear or reset your data structure to free memory / reset counts.
* **Conditional Build:** The `MAX_REQ` limit must not be hardcoded. It must be read at compile time via a preprocessor macro `#ifndef MAX_REQ ... #define MAX_REQ 3 ... #endif`.

### 2. The Build Script (`/home/user/build.sh`)
Write a bash script that compiles `rate_filter.c` into two different executables:
1. `/home/user/rate_filter_strict`: Compiled with `MAX_REQ` set to 2.
2. `/home/user/rate_filter_standard`: Compiled with `MAX_REQ` set to 5.
Ensure the script is executable and uses `gcc` with `-O2`.

### 3. Property-Based Testing (`/home/user/prop_test.py`)
Write a Python script that strictly verifies the logical properties of your rate filter.
* The script should generate exactly 10,000 random, chronologically ordered log lines spanning a simulated 100-second window, using a pool of 50 random IP addresses.
* It should pipe these lines into `/home/user/rate_filter_standard`.
* It must verify two properties on the output:
  1. **Upper Bound Property:** No IP address appears more than 5 times for any single timestamp.
  2. **Preservation Property:** If an IP address had `N` requests at a specific timestamp in the input, the output must contain exactly `min(N, 5)` requests for that IP at that timestamp.
* If both properties hold true, the script must write `"PASS"` to `/home/user/test_results.log` and exit with code 0. If either fails, it must write `"FAIL"` to the log and exit with a non-zero code.

Execute your build script and then execute your Python test script so that `/home/user/test_results.log` is generated.
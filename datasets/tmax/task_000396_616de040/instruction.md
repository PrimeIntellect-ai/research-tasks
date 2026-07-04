You are a QA Engineer setting up a test environment to validate a rate-limiting algorithm. The team has provided you with a file containing raw, out-of-order request logs encoded as hexadecimal timestamps.

Your task is to implement a C program that acts as a rate-limiting validator, and then use standard shell tools to run an integration test against expected results.

Here are the requirements for your C program:
1. Write a C program at `/home/user/qa_env/rate_check.c`.
2. The program must read line-by-line from `stdin` until EOF. Each line contains a 32-bit unsigned integer representing a UNIX timestamp, encoded as a hexadecimal string (e.g., `0x0000000B`).
3. Decode these hex strings into integer values and sort them in ascending chronological order.
4. Implement the rate-limiting validation logic: The maximum allowed rate is 3 requests per 10-second sliding window. This means any request that occurs within 10 seconds of the 3rd preceding request is considered a violation. Equivalently, in a 0-indexed sorted array of timestamps `t`, a request at index `i` (where `i >= 3`) is a violation if `t[i] - t[i-3] <= 10`.
5. Print all violating timestamps to `stdout` in standard base-10 integer format, one per line.

After writing the code, perform the following bash operations to complete the test setup:
1. Compile your program to `/home/user/qa_env/rate_check` using `gcc`.
2. Pipe the contents of `/home/user/qa_env/raw_requests.txt` into your compiled program, redirecting the standard output to `/home/user/qa_env/violations.log`.
3. Use the `diff` command to compare `/home/user/qa_env/violations.log` against the pre-existing baseline file `/home/user/qa_env/expected_violations.log`. Write the output of the diff command to `/home/user/qa_env/diff.log`. If the files match exactly, the diff log should be empty.

The environment directory `/home/user/qa_env/` and the input files already exist.
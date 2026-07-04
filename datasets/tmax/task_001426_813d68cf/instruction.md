You are a platform engineer troubleshooting a custom CI/CD pipeline that estimates build times based on module dependencies. The system recently updated its build configurations, and you need to determine how the build costs have changed, then expose this report via an internal proxy.

You have the following files in your environment:
1. `/home/user/costs_v1.txt`: A list of modules and their evaluated build costs from the previous release, formatted as `Module: Cost`.
2. `/home/user/formulas_v2.txt`: The new build cost formulas. Each line is formatted as `Module: Expression | Checksum`. 
   - `Expression` is a mathematical formula containing positive integers, addition (`+`), multiplication (`*`), and parentheses `()` representing the new build cost.
   - `Checksum` is a simple 8-bit integer validation code. It is calculated as the bitwise XOR sum of all ASCII characters strictly within the `Expression` string (including spaces, if any, exactly as written).

Your task consists of three phases:

**Phase 1: Expression Parsing and Checksum Validation (C Programming)**
Write a C program at `/home/user/evaluator.c` that reads `/home/user/formulas_v2.txt`.
For each line:
1. Extract the `Module`, `Expression`, and `Checksum`.
2. Compute the bitwise XOR sum of the characters in the `Expression` string.
3. Compare the computed checksum to the provided `Checksum`. If it does not match, silently skip the line.
4. If the checksum matches, parse and evaluate the mathematical expression (respecting standard precedence for `+`, `*`, and `()`).
5. Print the valid, evaluated module costs to standard output in the format `Module: Cost`.

**Phase 2: Sorting and Diffing**
1. Compile and run your C program, saving its exact output to `/home/user/costs_v2.txt`.
2. Sort both `/home/user/costs_v1.txt` and `/home/user/costs_v2.txt` alphabetically by the module name.
3. Generate a unified diff of the sorted v1 and sorted v2 files using the standard `diff -u` command. Save this diff to `/home/user/cost_diff.txt`. (Do not include timestamps in the diff header, or just let `diff -u` run normally; our verifier will check the core diff content).

**Phase 3: Reverse Proxy Configuration**
The CI/CD dashboard expects to fetch this diff via a specific endpoint.
1. Start a simple HTTP file server on port 9000 serving the directory `/home/user/`.
2. Write a lightweight reverse proxy script (e.g., in Python) at `/home/user/proxy.py`.
3. The proxy must listen on port 8080. When it receives an HTTP GET request to `/ci/diff`, it should proxy the request to your file server on port 9000 to fetch `/cost_diff.txt` and return its contents to the client with a `200 OK` status. Any other path should return `404 Not Found`.
4. Run both the file server and the reverse proxy in the background.

Verify your setup by running `curl http://localhost:8080/ci/diff` to ensure it outputs the correct unified diff.
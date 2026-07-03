You are a Site Reliability Engineer (SRE) monitoring uptime for a critical distributed system. Recently, the uptime log parser started dropping metrics. 

You have been provided with a screenshot of a bug report from the monitoring dashboard at `/app/error_report.png`. This image contains a snippet of the exact log timestamp format that is currently failing. 

There is a local Git repository at `/home/user/uptime_repo` containing the source code for the log parsing utility (`parse.py`). The parsing logic used to handle this edge case correctly, but a recent regression in the commit history broke it.

Your tasks are:
1. Analyze the image `/app/error_report.png` to identify the failing timestamp format edge case.
2. Use Git bisection in `/home/user/uptime_repo` to identify the exact commit that introduced the regression. 
3. Understand the subtle timezone/parsing bug introduced in that commit.
4. Write a standalone Python script at `/home/user/fixed_parser.py` that repairs the parsing logic. 

Requirements for `/home/user/fixed_parser.py`:
- It must take a single command-line argument representing the timestamp string.
- It must print the exact Unix epoch timestamp as a float (rounded to exactly 6 decimal places) to standard output.
- If the input string is completely invalid or cannot be parsed, it must print exactly `INVALID`.
- It must be extremely robust. An automated fuzzer will run thousands of randomly generated timestamp strings (including various edge cases, timezone transitions, and malformed strings) against your script and compare its output strictly against a pre-compiled oracle binary. Your script's output must be bit-exact equivalent to the oracle.

To succeed, ensure your timezone handling strictly respects standard Python `zoneinfo` rules and perfectly handles the edge case described in the image.
You are a developer investigating a regression in a mathematical expression evaluation service. 

There is a local Git repository at `/home/user/math_evaluator` containing a CLI tool `evaluate.py`. This tool accepts a JSON string containing a base64-encoded mathematical expression, decodes it, and attempts to parse and evaluate it. 

Usage: `python evaluate.py '{"expr_b64": "<base64_encoded_string>"}'`

Historically, `evaluate.py` was highly robust. If it encountered invalid math syntax, malformed JSON, or invalid byte encodings, it gracefully caught the errors, returning a JSON response like `{"error": "..."}` and exiting with a status code of `0`. 

However, a regression was introduced somewhere in the last 200 commits. The tool now crashes (exits with a non-zero status code, throwing an unhandled exception) when encountering specific edge-case binary/encoding sequences in the base64 payload. 

Your tasks are:
1. **Fuzz Testing:** Write a script to fuzz `evaluate.py` by generating various random or edge-case bytes, base64-encoding them, and passing them to the tool. Find a specific base64 payload that causes the tool to crash (exit code != 0).
2. **Bisection:** Use `git bisect` (the known good commit is `HEAD~200`, and the bad commit is `HEAD`) along with a script utilizing your discovered payload to automate the bisection process and find the exact commit that introduced the regression.
3. **Reporting:** 
   - Write the full 40-character Git commit hash of the first bad commit to `/home/user/bad_commit.txt`.
   - Write the exact base64 payload that triggers the crash to `/home/user/crash_payload.txt`.

Ensure your payload actually triggers the crash on the `HEAD` commit, but exits cleanly with `0` on the `HEAD~200` commit.
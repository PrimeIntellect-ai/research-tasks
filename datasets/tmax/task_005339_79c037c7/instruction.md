You are acting as a support engineer investigating a sudden failure in a mathematical parsing pipeline. The system processes custom mathematical expression logs, but it has started failing on certain edge-case formats containing scientific notation. 

The repository is located at `/home/user/poly_parser`. 

Here is your diagnostic checklist:
1. **Recover the Diagnostic Token**: We need to start a local diagnostic server to test the pipeline, but the `DIAGNOSTIC_TOKEN` was accidentally committed to a `.env` file and then hastily removed from the repository a few commits ago. Search the git history of the `/home/user/poly_parser` repository to find this token.
2. **Start the Diagnostic Server**: Once you have the token, run the server in the background: `python /home/user/poly_parser/diagnostic_server.py --token <YOUR_TOKEN> &`. Wait a few seconds for it to start.
3. **Find the Regression**: The parsing pipeline script `evaluate.py` is failing on the test file `edge_case.txt`. We know that the codebase was completely stable at the git tag `v1.0`. Use git bisection (or manual forensics) to find the exact commit hash that introduced the bug.
4. **Fix the Bug**: The bug is a format parsing edge-case issue in `evaluate.py`. A recent commit "optimized" a regular expression but accidentally broke the parsing of floating-point numbers in scientific notation (e.g., `COEFF(1.5e-4)`). Repair the regular expression in `evaluate.py` so that it correctly extracts the numeric string (including the exponent part) without changing the overall logic of the script.

When you are finished, you must create a JSON file at `/home/user/diagnostics.json` with the following structure:
```json
{
  "diagnostic_token": "<the extracted token>",
  "bad_commit": "<the full 40-character commit hash of the regression>",
  "service_status": "running"
}
```

Verify your fix by running `python /home/user/poly_parser/evaluate.py --test edge_case.txt`. It should complete successfully and print the parsed float without raising a `ValueError`. Do not commit your fix to the repository, just leave the file modified.
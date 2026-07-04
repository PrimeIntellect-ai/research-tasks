You are tasked with debugging a data processing pipeline that recently started failing with an `IndexError` during the nightly batch jobs. The issue seems to be caused by certain edge-case payloads that the code no longer handles correctly.

The codebase is located in a Git repository at `/home/user/data_processor`.
The input data for testing is located at `/home/user/input.json`.

Your objectives are:
1. **Error Diagnosis & Bisection**: Analyze the stack trace when running the code on the input data. Use Git bisection to find the exact commit that introduced the bug.
2. **Report**: Write the full 40-character SHA of the offending commit to `/home/user/bad_commit.txt`.
3. **Fix**: Patch the bug in `processor.py` so that it handles edge-case data gracefully. If the required index does not exist in the tokens list, the `extract_code` function should return `None` rather than crashing.
4. **Validation**: Run the script successfully using the command: `python run.py /home/user/input.json /home/user/output.json`.

Ensure that the output file `/home/user/output.json` is generated successfully and the program exits with code 0.
You are a DevOps engineer tasked with debugging and securing a mathematical query logging system. 

Recently, the system started experiencing anomalies, and the original developer left without leaving complete documentation. You need to fix the query parser, find a critical missing parameter, and build a log classifier to filter out malicious ("evil") queries.

Here is your multi-stage task:

1. **Information Extraction**:
   There is a screenshot of the legacy monitoring dashboard located at `/app/sys_monitor.png`. You must analyze this image (using OCR tools like `tesseract`, which is available) to extract the numeric value for the `CRITICAL SYSTEM SALT`.

2. **Environment & Build Repair**:
   We use a custom Python C-extension for fast query evaluation located in a local Git repository at `/app/math_parser_repo`. Currently, it fails to build. Diagnose the environment misconfiguration or build failure in the repository (e.g., in `setup.py` or missing compiler flags) and fix it so that `pip install -e .` succeeds.

3. **Regression Finding (Git Bisection)**:
   Even after it builds, the `math_parser` has a regression. It incorrectly evaluates the results of certain mathematical queries due to a recently introduced bug. Use `git bisect` to identify the faulty commit in `/app/math_parser_repo`, then revert or fix the code so the parser works correctly on all edge cases.

4. **Adversarial Log Classification**:
   Write a Python script at `/home/user/log_classifier.py`.
   Your script must accept a single command-line argument (the path to a log file).
   Each log file contains a JSON object with a `query_value` (integer) and a `reported_hash` (integer).
   Your script must:
   - Import the fixed `math_parser` module.
   - Use `math_parser.compute_hash(query_value, CRITICAL_SYSTEM_SALT)` to calculate the true hash.
   - Compare the computed hash to the `reported_hash`.
   - **Exit with code 0** if the log is clean/valid (the hashes match).
   - **Exit with code 1** if the log is evil/anomalous (the hashes do not match).

We have provided two directories containing log files for you to test your script:
- `/app/corpus/clean/` (contains only valid logs)
- `/app/corpus/evil/` (contains only anomalous logs)

To complete the task successfully, your script `/home/user/log_classifier.py` must achieve 100% accuracy: rejecting all evil logs (exit code 1) and preserving all clean logs (exit code 0).
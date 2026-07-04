You are acting as a support engineer collecting diagnostics for a failing backend service. You have been granted access to a Linux terminal.

Your client has an optimization package located at `/home/user/optimization_project`. The client reported three distinct issues with this repository:
1. **Security Leak:** A developer accidentally hardcoded a production API key in the codebase recently. They supposedly removed it in a later commit, but the client is worried the secret is still buried in the git history.
2. **Build Failure:** The package includes a C-extension for performance, but compiling it via `python3 setup.py build_ext --inplace` fails with a linker error related to missing math symbols.
3. **Algorithm Convergence Failure:** The primary numerical solver in `optimizer.py` is failing to converge and raises a "Convergence failure: Max iterations reached" exception.

Your tasks:
1. **Recover the Secret:** Analyze the git history of `/home/user/optimization_project` to find the leaked production API key.
2. **Fix the Build:** Modify `/home/user/optimization_project/setup.py` so that the C-extension compiles and links correctly.
3. **Fix the Convergence:** Debug and fix the numerical algorithm in `/home/user/optimization_project/optimizer.py`. The function is trying to find the root of $f(x) = x^3 - 2x - 5$ using Newton's method. The implementation has a mathematical bug preventing convergence within the allotted iterations.
4. **Run Diagnostics:** Once the code is compiled and fixed, run `python3 run_diagnostics.py`. This will generate a file named `/home/user/optimization_project/SUCCESS_REPORT.txt`.

Finally, create a master diagnostic report at `/home/user/diagnostics.txt` with the following exact format:
```
SECRET_KEY: <The leaked API key you found in the git history>
DIAGNOSTICS:
<Paste the complete contents of /home/user/optimization_project/SUCCESS_REPORT.txt here>
```
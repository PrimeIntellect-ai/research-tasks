You are the on-call engineer and just received a 3 AM page. The staging environment for our Python-based data processing microservice just crashed, and to make matters worse, the automated CI/CD build is currently failing, preventing us from deploying a fix. 

You need to investigate the crash and fix the build. Here is what we know:

1. **Build Failure Diagnosis**: The build script located at `/home/user/app/build.py` is failing. Diagnose and fix the script so that running `python /home/user/app/build.py` exits with code 0 and successfully prints "Build complete".

2. **Memory Dump Analysis**: When the staging service crashed, it dumped its memory to `/home/user/app/memory.dmp`. You need to extract the exact crash reference ID from this binary file. The ID is an alphanumeric string immediately following the text `CRASH_REF: ` (e.g., `CRASH_REF: <ID_HERE>`). Once you find it, write just the extracted ID (no extra text or spaces) to `/home/user/crash_ref.txt`.

3. **Regression Test Construction**: We need to ensure this specific crash is caught in the future. The application logic is in `/home/user/app/processor.py`. Create a Python test file at `/home/user/app/test_regression.py` using the standard `unittest` library. Your test must:
   - Import the `process` function from `processor`.
   - Call `process()` passing the crash reference ID you extracted from the memory dump.
   - Explicitly assert that a `RuntimeError` is raised when this specific ID is processed.

Your task is complete when `build.py` runs successfully, the correct ID is in `crash_ref.txt`, and running `python -m unittest /home/user/app/test_regression.py` executes your test and passes without failures.
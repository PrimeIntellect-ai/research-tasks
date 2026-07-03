I am a developer trying to debug a failing build process for our data aggregation pipeline. 

The build script is located at `/home/user/project/build.py`. When I run it (`python3 /home/user/project/build.py`), it fails and prints a generic "Build failed with an encoding error!" message, but it completely swallows the exception and doesn't tell me which file caused the crash. 

The script reads hundreds of text files from `/home/user/project/data/` and tries to serialize their contents into a single JSON file. One of the files contains an invalid byte sequence that crashes the standard UTF-8 decoder.

Your tasks are:
1. **System Call Tracing:** Use `strace` or a similar tool to trace the execution of `build.py` and identify exactly which file in the `data/` directory is causing the process to crash.
2. **Record the Culprit:** Once you find the bad file, write its basename (e.g., `file_123.txt`) to `/home/user/bad_file.log`.
3. **MRE Creation:** Create a minimal reproducible example script at `/home/user/mre.py`. This script should be a bare-minimum Python script that reads *only* the specific bad file you identified (using the default `open(..., 'r')` mode) and triggers the exact underlying `UnicodeDecodeError`.
4. **Fix the Build:** Modify `/home/user/project/build.py` to fix the encoding issue. Specifically, update the `open()` call inside the script to use `encoding='utf-8'` and `errors='replace'`.
5. **Verify:** Run the fixed `build.py` script so that it successfully generates `/home/user/project/output.json`.

Please complete all these steps. I will verify the fix by checking for the existence of `output.json`, the correctness of `bad_file.log`, and the contents of `mre.py`.
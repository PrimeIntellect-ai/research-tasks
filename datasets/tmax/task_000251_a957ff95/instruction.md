You are a developer debugging a failing build process. The main build script located at `/home/user/project/build.py` keeps crashing intermittently with a `FileNotFoundError`. 

The script spawns a couple of threads to handle manifest generation and cache cleanup simultaneously. However, due to a combination of a race condition and a subtle timezone handling bug, a critical intermediate file is being deleted before the main build step can consume it.

Your task:
1. Analyze `/home/user/project/build.py` and its traceback to diagnose the problem.
2. Identify the root cause of the premature file deletion (hint: look closely at how the cleanup thread calculates file age).
3. Fix the bug in `/home/user/project/build.py` so that the script executes successfully without throwing exceptions.

When you have successfully fixed the script, running `python3 /home/user/project/build.py` should exit with code 0 and successfully generate the file `/home/user/project/build_artifact.txt`. The automated test will verify that this artifact file exists and contains the correct success payload. Do not change the final output format or the directory structure.
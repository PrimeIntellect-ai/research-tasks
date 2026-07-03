You are an engineer investigating a critical issue in a long-running Python service located at `/home/user/service_repo`. 

Recently, two things happened:
1. The latest commit broke the local environment setup due to a dependency conflict/error in `requirements.txt`, preventing the service from even running.
2. A previous commit introduced a severe bug: the service hangs and consumes unbounded memory (a memory leak caused by an infinite loop) under certain conditions.

Your tasks:
1. Resolve the dependency issue in `/home/user/service_repo/requirements.txt` so the dependencies can be successfully installed via `pip install -r requirements.txt`.
2. Use Git bisection (or manual commit inspection) to identify the exact commit hash that introduced the memory leak / infinite loop.
3. Fix the infinite loop bug in `/home/user/service_repo/processor.py` on the `main` branch so the script runs successfully and terminates.
4. Create a file at `/home/user/bug_info.txt` containing the exact Git commit hash that originally introduced the bug, in the following format:
   `Bad Commit: <commit_hash>`

Ensure that by the end of your task, running `python3 /home/user/service_repo/processor.py` completes successfully without hanging.
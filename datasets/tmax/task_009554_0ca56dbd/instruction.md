You are an IT support technician working on a ticket (#4092) regarding an internal Python tool that computes a final tally of jobs processed. The script is located at `/home/user/ticket_4092/process_jobs.py`. 

Users are reporting that the script's output is inconsistent. It is supposed to always output `1000000`, but it frequently outputs smaller, random numbers. 

Your task is to:
1. Identify and fix the race condition in `/home/user/ticket_4092/process_jobs.py` so that it safely increments the global counter. You can use standard Python concurrency primitives (e.g., from the `threading` module). The final print statement must reliably output `1000000`.
2. Write a bash regression test script at `/home/user/ticket_4092/regression_test.sh`. This script must run the `process_jobs.py` script exactly 10 times. 
   - If the python script outputs `1000000` for all 10 runs, the bash script must exit with a status code of `0`.
   - If the python script outputs any other value during any of the runs, the bash script must immediately exit with a status code of `1`.
3. Ensure that `/home/user/ticket_4092/regression_test.sh` is executable.

You have all standard Linux shell tools and Python 3 available to diagnose and complete this task.
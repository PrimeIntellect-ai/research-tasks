You are a DevOps engineer responsible for maintaining a Python-based log processing service. The service has been intermittently crashing in production. The system logs show occasional `ValueError: math domain error` exceptions coming from the statistics module.

The codebase is located in `/home/user/app/`. 
You have the following files:
- `/home/user/app/processor.py`: Contains the core logic for calculating statistics from log data batches.
- `/home/user/app/runner.py`: A script that simulates the production data stream and intermittently reproduces the failure.
- `/home/user/app/verify.py`: A verification script.

Your task:
1. Analyze the existing codebase and use `runner.py` to reproduce the intermittent crash and get the stack trace.
2. Diagnose the root cause of the crash. The issue is caused by numerical instability in the algorithm used to calculate the standard deviation when processing specific edge-case data.
3. Fix the `compute_statistics(data)` function in `/home/user/app/processor.py` to prevent this crash while still correctly calculating the mean and standard deviation. You may change the formula to a numerically stable one or clamp intermediate floating-point inaccuracies safely.
4. Once you have applied your fix, run `python /home/user/app/verify.py`. If your fix is correct, this script will complete successfully and generate a log file at `/home/user/app/success.log`.

Do not modify `/home/user/app/verify.py` or `/home/user/app/runner.py`. Your fix must be contained entirely within `/home/user/app/processor.py`. The presence of a valid `/home/user/app/success.log` file with the correct expected output will be used to verify your completion of this task.
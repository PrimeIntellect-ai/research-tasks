You are an IT support technician resolving Ticket #4092. 

A user has reported that their mathematical computation tool, located at `/home/user/math_tool/compute.py`, is crashing and failing to produce its report. 

Here are the details from the user's ticket:
1. The script is supposed to compute the 5000th term of the Fibonacci sequence, modulo 100000 (where F(0) = 0, F(1) = 1).
2. Recently, someone modified the script. Now it crashes with a traceback or core dump before completing the calculation. You need to analyze the crash, identify the flawed mathematical logic (which was changed to a poorly implemented recursive approach), and fix the Python code to compute the correct result efficiently without crashing.
3. The script attempts to write the output to a file, but the path was obfuscated and broken in the recent update. Use system call tracing (e.g., `strace`) to figure out what unauthorized absolute file path the script is trying to open. Once you find it, modify the script to write the output instead to `/home/user/result.txt`.
4. The script previously contained a hardcoded API key used for reporting. The user accidentally committed it, then tried to remove it in the latest commit, but they lost the key entirely. You need to perform git history forensics on the repository at `/home/user/math_tool/` to recover this lost API key.

To resolve the ticket, perform the following actions:
1. Recover the lost API key and write it to `/home/user/recovered_key.txt`.
2. Fix the mathematical logic in `/home/user/math_tool/compute.py` so it correctly calculates the 5000th Fibonacci number modulo 100000.
3. Fix the output file path in the script so it writes the final integer result to `/home/user/result.txt`.
4. Run the fixed script to ensure `/home/user/result.txt` is generated correctly.
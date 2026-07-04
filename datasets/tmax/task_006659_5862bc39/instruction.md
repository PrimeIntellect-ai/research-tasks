You are a security researcher analyzing a suspicious Python repository containing a mathematical utility. The repository is located at `/home/user/suspicious_repo`. 

Recently, automated monitors flagged that the script `check_prime.py` occasionally fails with an unexpected crash (exit code 139) on specific inputs, despite appearing to just be a simple primality tester.

Your objectives:
1. **Fuzz Testing:** The script takes a single integer argument. Write a quick shell loop to test `python3 check_prime.py <N>` for integers `N` between 1 and 1000 to find the exact input that causes the script to crash with exit code 139.
2. **System Call Tracing:** Run the script with the crashing input using `strace`. Observe the system calls to find a suspicious hidden file in `/tmp/` that the script attempts to open (it starts with `/tmp/.backdoor_`) right before it crashes.
3. **Regression Finding:** The repository uses Git. Find the exact Git commit hash (the full 40-character hash) that introduced this crashing behavior/backdoor. The `main` branch currently has several commits, and the initial commit was completely clean.

Write your findings to a file named `/home/user/investigation.txt` with exactly three lines in the following format:
Line 1: The crashing integer input
Line 2: The full absolute path to the `/tmp/` backdoor file
Line 3: The full 40-character Git commit hash that introduced the backdoor

Do not write anything else in `/home/user/investigation.txt`.
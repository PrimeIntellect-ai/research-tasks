You are an operations engineer triaging an incident. A backup rotation system has been failing. The main script `/home/user/backup_repo/backup_manager.sh` is stuck in an infinite loop and, when forcefully terminated, produces incorrect negative byte counts due to numerical instability (Bash signed integer overflow). Additionally, an API key required for the backups was accidentally committed to the Git repository in the past, then poorly removed, and is now lost.

Your tasks are:
1. Conduct Git history forensics in `/home/user/backup_repo` to recover the lost API key. Write the exact value of the API key to `/home/user/api_key.txt`.
2. Diagnose and fix the infinite loop in `/home/user/backup_repo/backup_manager.sh`.
3. Fix the numerical instability in the script. The script attempts to sum very large byte values that exceed Bash's 64-bit signed integer limit (9,223,372,036,854,775,807). Modify the script to use `bc` or `awk` to correctly calculate and print the sum.
4. Run the fixed script and redirect its standard output to `/home/user/output.txt`. The final output line should read exactly: `Total bytes: <correct_sum>`.

Ensure all fixed code remains in Bash (using standard CLI tools like `bc` or `awk` for math) and does not indefinitely hang.
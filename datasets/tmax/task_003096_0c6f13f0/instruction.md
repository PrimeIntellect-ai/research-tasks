You are an IT support technician. We have received Ticket #8841 regarding a broken internal script.

The script `/home/user/ticket_8841/sum_values.sh` is designed to recursively find all `.txt` files within a given target directory, read the single integer value inside each file, and compute the total sum of these values. Finally, it must multiply this sum by an environment variable named `MATH_SCALE` and output the final result.

Users are reporting that the script throws errors and returns incorrect results because several files and subdirectories in the data repository have spaces in their names. Furthermore, the script has an environment misconfiguration where it overrides or ignores the `MATH_SCALE` variable provided by the system.

Your task:
1. Debug and fix `/home/user/ticket_8841/sum_values.sh` so that it correctly handles filenames and directories with spaces (and other unusual characters).
2. Ensure it properly uses the system-provided `MATH_SCALE` environment variable for its final multiplication.
3. Run your fixed script against the directory `/home/user/ticket_8841/data/`.
4. Save the final calculated integer output by the script into a file named `/home/user/ticket_8841/result.txt`.

Note: The system environment has already exported `MATH_SCALE` for you. You must use `Bash` to fix the script.
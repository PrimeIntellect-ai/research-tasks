You are a performance engineer tasked with fixing a broken data processing pipeline on a Linux system.

A critical data file, `/home/user/data.csv`, was accidentally deleted by an automated cleanup script. Fortunately, you suspect a background monitoring process might still have the file descriptor open, allowing for recovery.

Additionally, the Python script that processes this data, `/home/user/process_data.py`, is failing. It is supposed to calculate the population standard deviation of the numbers in the dataset. However, it suffers from two major issues:
1. It crashes on corrupted or malformed lines.
2. It suffers from numerical instability (catastrophic cancellation) when dealing with datasets that have very large means and small variances, resulting in a `ValueError: math domain error`.

Your task:
1. Recover the deleted file and save it exactly as `/home/user/recovered_data.csv`.
2. Fix the Python script `/home/user/process_data.py` so that it:
   - Reads from `/home/user/recovered_data.csv`.
   - Silently ignores any lines that cannot be successfully parsed as floats.
   - Calculates the **population standard deviation** correctly without numerical instability.
   - Writes the final calculated standard deviation to `/home/user/result.txt`, rounded to 4 decimal places (e.g., `0.1234`).
3. Run the fixed script to generate `/home/user/result.txt`.

Do not change the fundamental goal of the script (computing population standard deviation), but you may use standard library modules to fix the numerical instability.
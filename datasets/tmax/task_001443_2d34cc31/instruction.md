I was bisecting a mathematical regression across 200 commits in my Python scientific library. Sometime recently, our `delta_calc` function started returning `0.000000000000000` for large inputs due to floating-point precision loss (catastrophic cancellation). 

I have an older, known-good compiled C binary located at `/app/oracle_calc` that computes the exact same mathematical function correctly and avoids the precision loss. Unfortunately, the binary is stripped, and the original C source code is lost. 

To make matters worse, while trying to debug this, I accidentally deleted a text file called `notes.txt` from my loopback development drive `/home/user/dev_drive.img`. That file contained important notes about the underlying mathematical formula the binary was designed to evaluate.

Your task is to:
1. Mount or inspect the ext4 image `/home/user/dev_drive.img` and recover the deleted `notes.txt` file (I just used standard `rm` on it). Read it to get the mathematical context.
2. Reverse engineer or analyze the stripped binary `/app/oracle_calc` alongside the recovered notes to determine the exact function being computed and how it avoids precision loss.
3. Write a Python script at `/home/user/solution.py` that takes a single float `x` as a command-line argument and prints the evaluated result formatted to 15 decimal places (e.g., `print(f"{result:.15f}")`).

Your Python implementation must perfectly match the numerical output of `/app/oracle_calc` for any non-negative floating-point input, specifically fixing the catastrophic cancellation issue for very large values of `x` (e.g., `x = 1e12`). 

Ensure your final script is robust, uses standard Python libraries only (like `math`), and properly accepts standard float strings.
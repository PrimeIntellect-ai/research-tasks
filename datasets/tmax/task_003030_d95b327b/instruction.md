You are a bioinformatics analyst working with sequence mutation rate data. A recent upstream matrix factorization step failed on near-singular sequence alignments, producing `NaN` values for several sequence pairs. 

Your task is to write a pure Bash/CLI script to calculate a robust bootstrap confidence interval for the mutation rates, bypassing the failures and proving statistical convergence, which will serve as a regression test baseline.

Create a script at `/home/user/bootstrap_ci.sh` that takes two arguments: `<input_file>` and `<num_iterations>`.
The script must perform the following:
1. Read the input file and filter out any lines containing exactly `NaN`.
2. Let `N` be the number of valid numeric lines remaining.
3. Perform a bootstrap loop for `<num_iterations>` times. In each iteration:
   - Sample `N` values from the valid data *with replacement*. (You may use standard tools like `shuf`, `awk`, etc.).
   - Calculate the arithmetic mean of this sample.
4. Keep track of these bootstrap means. 
5. **Convergence Testing:** Every 100 iterations (at i=100, 200, 300, etc.), calculate the cumulative average of all the bootstrap means calculated *up to that point*. Append this cumulative average to `/home/user/convergence.txt` in the format: `Iteration <i >: <cumulative_average>`.
6. **Confidence Intervals:** After completing all iterations, sort the bootstrap means. Find the 2.5th percentile and the 97.5th percentile to form the 95% confidence interval. (For example, if you have 1000 iterations, these correspond to the 25th and 975th values in the sorted list).
7. Write the final CI to `/home/user/ci_output.txt` in the exact format: `Lower: X.XXX, Upper: Y.YYY` (rounded to 3 decimal places).

Once your script is written, execute it on the provided data file `/home/user/mutation_rates.txt` using exactly `1000` iterations. 

Constraints:
- Use only Bash, coreutils, `awk`, `sed`, or other standard POSIX CLI utilities. Do not write Python, Perl, or R scripts.
- Ensure your output files (`ci_output.txt` and `convergence.txt`) are created and populated correctly.
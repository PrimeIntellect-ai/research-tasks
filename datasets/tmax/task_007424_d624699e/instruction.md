As a performance engineer, I am profiling a bioinformatics pipeline that computes statistics over large sets of genetic sequences. We suspect that our current variance calculation suffers from catastrophic cancellation (numerical instability) when dealing with extremely small variances in shifted datasets.

I have placed a dataset of 10,000 sequences in `/home/user/dataset.fasta`. 

Your task is to write and run a Python script at `/home/user/profile_gc.py` that does the following:
1. Parses `/home/user/dataset.fasta` and extracts all sequences (ignore the headers).
2. Uses Python's `multiprocessing.Pool` with exactly 4 worker processes to compute the GC ratio (the number of 'G' and 'C' characters divided by the total length of the sequence) for every sequence in parallel.
3. To stress-test the numerical stability of our algorithms, add exactly `100000000.0` ($10^8$) to every computed GC ratio. Let's call this list of shifted values $S$.
4. Calculate the population variance of $S$ using two different methods:
   - **Naive Method:** Use the standard formula $Var(S) = \frac{\sum x^2}{N} - (\frac{\sum x}{N})^2$ implemented with standard Python `float` arithmetic and built-in `sum()`.
   - **Stable Method:** Use Python's built-in `statistics.pvariance()`, which uses a numerically stable two-pass algorithm.
5. Write the results to a file located at `/home/user/report.txt`. The file must contain exactly two lines in this format, with values formatted to 10 decimal places in scientific notation (e.g., `1.2345678900e-05`):
   ```text
   Naive: <naive_variance>
   Stable: <stable_variance>
   ```

Ensure your script is self-contained and handles the parallel processing safely. Execute your script to generate `/home/user/report.txt`.
You are a bioinformatics analyst investigating GC content fluctuations across a set of aligned DNA sequences. You must process this sequence data into a numerical signal, compute statistical confidence intervals, and visualize the results. 

Your entire solution must be implemented using ONLY Bash, Awk, and standard coreutils (e.g., `grep`, `sort`, `sed`). Do NOT use Python, R, Perl, or any other scripting languages to process the data or calculate statistics.

**Data:**
You are provided with a FASTA file at `/home/user/sequences.fasta` containing 50 aligned DNA sequences, each exactly 100 bases long.

**Requirements:**

1. **Signal Data Processing (Sliding Window):**
   Convert each sequence into a numerical signal representing the GC fraction (count of 'G' or 'C' divided by window size). Use a sliding window of size 10 with a step size of 1. 
   - Position 1 is bases 1-10, Position 2 is bases 2-11, ..., Position 91 is bases 91-100.
   - For each of the 50 sequences, you should compute 91 GC fraction values.

2. **Statistical Analysis (Bootstrap Confidence Intervals):**
   For each of the 91 sliding window positions, calculate the true sample mean GC fraction across all 50 sequences.
   Then, perform bootstrap resampling (with replacement) to estimate the 95% confidence interval for the mean.
   - Use exactly `B=100` bootstrap iterations.
   - For each iteration, randomly sample 50 values (with replacement) from the 50 sequence values at that position, and compute the bootstrap mean.
   - To ensure reproducibility in the automated tests, you MUST use the following Linear Congruential Generator (LCG) logic in Awk for random sampling, rather than `rand()`. 
     Initialize a global seed `seed = 42` at the start of your script.
     Every time you need a random index (from 1 to 50), update the seed and calculate the index as follows:
     ```awk
     seed = (seed * 1103515245 + 12345) % 2147483648
     idx = int((seed / 2147483648) * 50) + 1
     ```
     *(Note: Perform the resampling for Position 1 (100 iterations, each drawing 50 samples = 5000 random numbers), then Position 2, etc., sequentially, maintaining the global seed state throughout.)*
   - Calculate the 2.5th and 97.5th percentiles of the 100 bootstrap means to determine the LowerCI and UpperCI. (Since B=100, sort the bootstrap means and pick the 3rd value for LowerCI and 98th value for UpperCI, assuming 1-based indexing).

3. **Output Format:**
   Save the results to `/home/user/gc_bootstrap.tsv`. The file must be tab-separated, have NO header, and contain exactly 4 columns:
   `Position` `Mean` `LowerCI` `UpperCI`
   *(Format numerical values to 4 decimal places).*

4. **Visualization:**
   Write a Gnuplot script at `/home/user/plot.gp` that reads `/home/user/gc_bootstrap.tsv` and generates a PNG image at `/home/user/gc_plot.png`.
   - The plot should have "Position" on the X-axis and "GC Fraction" on the Y-axis.
   - Plot the Mean as a solid line.
   - Plot the confidence interval (LowerCI to UpperCI) as a shaded region or filled curves behind the mean line.

Ensure all outputs are placed exactly where specified.
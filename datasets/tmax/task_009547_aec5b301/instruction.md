As a bioinformatics analyst, you need to determine the required sample size to reliably estimate the GC content of a newly sequenced library. You will analyze a reproducible pipeline, check for convergence, and compare against a reference dataset.

You are provided with a FASTA file at `/home/user/bio_data/sequences.fasta` and a reference GC content value in `/home/user/bio_data/reference_gc.txt`.

Your task is to write a Python script that does the following:
1. Iteratively computes the cumulative average GC content (total G and C bases divided by total bases) of the first $N$ sequences in the FASTA file, starting from $N=10$ and incrementing by 10 (i.e., $N=10, 20, 30, \dots$).
2. Checks for convergence: We consider the cumulative GC content to have converged at step $N$ if the absolute difference in cumulative GC content between the current step and the previous step (e.g., $|GC_{N} - GC_{N-10}|$) is strictly less than $0.005$ for **three consecutive step increments**. The converged sample size is the $N$ at the end of these three increments (for example, if the absolute differences at $N=20$ vs $10$, $N=30$ vs $20$, and $N=40$ vs $30$ are all $< 0.005$, then the converged sample size is $N=40$).
3. Calculates the absolute difference between the cumulative average GC content at the converged $N$ and the reference GC content from the text file.
4. Outputs the final result as a JSON file at `/home/user/result.json` with the following keys:
   - `"converged_N"`: integer, the converged sample size.
   - `"average_gc"`: float, the cumulative average GC content at `converged_N`, rounded to 5 decimal places.
   - `"reference_gc"`: float, the reference GC content from the text file, rounded to 5 decimal places.
   - `"difference"`: float, the absolute difference between `average_gc` and `reference_gc`, rounded to 5 decimal places.

Make sure your script correctly reads the FASTA format, ignores the header lines starting with `>`, and only counts the sequence lines.
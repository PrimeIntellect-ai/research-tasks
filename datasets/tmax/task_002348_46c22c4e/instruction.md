You are a bioinformatics analyst trying to identify periodic signals in a set of DNA sequences. We are using a third-party bash/awk toolkit called `bio-spectral`, which performs spectral analysis on nucleotide sequences to find periodic patterns (often indicative of structural properties). 

However, there is an issue. The toolkit is located at `/app/bio-spectral-v1.0`. When running it on our dataset at `/home/user/sequences.fasta`, it crashes on some sequences because of a linear detrending step that fails with a "division by zero" error when a sequence has a highly uniform local composition (which causes a near-singular matrix in the detrending equation). 

Your tasks are as follows:
1. Identify and fix the bug in `/app/bio-spectral-v1.0/detrend.awk` that causes the script to crash on uniform sequences. You should add a small regularization factor (`epsilon = 1e-6`) to the variance denominator to prevent division by zero.
2. Use the fixed toolkit to compute the spectral score for every sequence in `/home/user/sequences.fasta`. The main script to run is `/app/bio-spectral-v1.0/run_spectral.sh <sequence_string>`.
3. Identify the sequence ID and sequence string that yields the highest spectral score.
4. To establish statistical significance, perform a Monte Carlo simulation. Generate 100 random permutations (shuffles) of this top-scoring sequence. Compute the spectral score for each permutation using the toolkit.
5. Calculate the empirical p-value for the top sequence. The p-value is the proportion of the 100 permutations that have a spectral score greater than or equal to the original top sequence's score.
6. Write your final results to `/home/user/result.txt` with exactly three lines in this format:
   ```
   Top_ID: <Sequence_ID>
   Top_Score: <Score>
   P-value: <p_value>
   ```

Constraints:
- Use only standard Bash, `awk`, `sed`, `grep`, and `bc`.
- The `run_spectral.sh` script outputs a single floating-point number representing the score.
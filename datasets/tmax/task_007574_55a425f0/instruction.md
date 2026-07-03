You are a performance engineer working on optimizing a bioinformatics pipeline. Your team needs a highly optimized, reproducible Bash script to parse FASTA files, compute sequence lengths, and calculate a bootstrap confidence interval for the mean sequence length. 

Your task is to create a Bash script at `/home/user/fast_bootstrap.sh` that takes exactly two arguments:
1. The path to a FASTA file.
2. An integer random seed.

The script must perform the following steps:
1. **Parse the FASTA file**: Extract the length of each sequence. A sequence record starts with a header line beginning with `>`. The actual sequence may be split across multiple lines.
2. **Compute Original Mean**: Calculate the mean length of all sequences in the file.
3. **Bootstrap Resampling**: Use `gawk` to generate 1000 bootstrap samples (with replacement) of the sequence lengths. To ensure reproducibility and match the automated test expectations, you **must** use `gawk` and structure your random sampling exactly as follows:
   - Initialize the random number generator in the `BEGIN` block using `srand(seed)`, where `seed` is the second argument passed to your script.
   - Loop for 1000 iterations (the bootstrap samples).
   - In each iteration, loop `N` times (where `N` is the total number of sequences).
   - Draw a random index using the exact formula: `idx = int(rand() * N) + 1`.
   - Calculate the mean sequence length for each of the 1000 bootstrap samples.
4. **Compute Confidence Interval**: Sort the 1000 bootstrap means in ascending order. The 95% confidence interval is defined by the 2.5th percentile (the 25th value in the sorted list) and the 97.5th percentile (the 975th value).
5. **Output**: Print the results to standard output in exactly the following format, rounding to 2 decimal places:

```
Original Mean: <mean>
95% CI: <lower> to <upper>
```

**Constraints**:
- The script must be executable (`chmod +x`).
- You must use standard Linux utilities (like `gawk`, `sort`). Python or other scripting languages are not allowed for the core logic.
- Ensure the script is highly efficient.

You can test your script against the provided file `/home/user/input.fasta` using a seed of your choice (e.g., `./fast_bootstrap.sh /home/user/input.fasta 123`). When you are confident the script works and produces reproducible outputs given the same seed, you have completed the task.
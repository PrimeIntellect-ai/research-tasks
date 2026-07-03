You are a Machine Learning Engineer preparing a dataset of genomic features for a model that predicts amplification efficiency. 

You have a reference dataset of DNA sequences located at `/home/user/sequences.fasta`. 
Your task is to extract a specific numerical feature from a subset of these sequences and calculate its bootstrap confidence interval.

Please write and execute a Python script to perform the following steps:

1. **Primer Sequence Alignment**: 
   Filter the sequences in `/home/user/sequences.fasta`. Keep only the sequences that contain the primer sequence `ACTGGCCTA` with **at most 1 mismatch** (i.e., exactly 0 or 1 character difference in any contiguous substring of length 9).

2. **Feature Extraction (Matrix Decomposition)**:
   For each filtered sequence, convert the *entire* sequence into a 2D One-Hot Encoded matrix where each row represents a nucleotide in the order it appears, mapped as follows: 
   A = [1, 0, 0, 0]
   C = [0, 1, 0, 0]
   G = [0, 0, 1, 0]
   T = [0, 0, 0, 1]
   (Ignore any sequences containing non-ACGT characters, though the dataset should only contain ACGT).
   For each resulting $N \times 4$ matrix, compute the **largest singular value** ($\sigma_1$) using Singular Value Decomposition (SVD).

3. **Bootstrap Confidence Interval**:
   You will now have an array of top singular values (one for each filtered sequence). Calculate the 95% bootstrap confidence interval for the **mean** of these singular values.
   - Use exactly 10,000 bootstrap resamples (sample with replacement).
   - Use `numpy` and set `numpy.random.seed(42)` immediately before running the bootstrap loop/function to ensure reproducibility.
   - Use the 2.5th and 97.5th percentiles of the bootstrap distribution to define the lower and upper bounds.

4. **Output**:
   Save the confidence interval to a JSON file at `/home/user/features_ci.json` with the following exact format:
   ```json
   {
       "ci_lower": 1.2345,
       "ci_upper": 5.6789
   }
   ```
   (Round the values to 4 decimal places).
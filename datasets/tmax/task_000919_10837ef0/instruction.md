You are a bioinformatics analyst evaluating the specificity of a new primer design. You need to determine if the primer aligns to a target sequence significantly better than it would to a random sequence of the same length.

There is an HDF5 file located at `/home/user/assay_data.h5` containing two datasets at the root level:
- `/target`: The target DNA sequence (stored as an ASCII string).
- `/primer`: The primer DNA sequence (stored as an ASCII string).

Your task is to write a script in any language you prefer to do the following:

1. Read the `target` and `primer` sequences from the HDF5 file.
2. Define the Maximum Match Score (MMS) as the maximum number of matching nucleotides (at the same relative positions) between the primer and any contiguous substring of the target sequence that has the same length as the primer.
3. Calculate the observed MMS of the primer against the true target sequence.
4. Perform a Monte Carlo simulation to estimate the background distribution of the MMS. Generate 50,000 independent random DNA sequences of the same length as the target sequence. For each sequence, each nucleotide (A, C, G, T) must have exactly a 25% chance of occurring at each position.
5. Calculate the MMS of the primer against each of the 50,000 random sequences.
6. Compute the empirical mean and standard deviation of these 50,000 background MMS values.
7. Calculate the Z-score of the observed MMS against this background distribution: `Z = (observed_MMS - mean) / std`.
8. Save the results to `/home/user/alignment_stats.json` with the following exact JSON schema:
```json
{
  "observed_mms": <integer>,
  "background_mean": <float>,
  "background_std": <float>,
  "z_score": <float>
}
```

Since you are running a Monte Carlo simulation, your mean, std, and z-score results will have slight variance. We will verify your output by checking if your values fall within a tight, statistically sound tolerance (±0.05) of the true expected values.

Ensure your code handles dependencies properly (e.g., if you use Python, you may need to `pip install h5py numpy`).
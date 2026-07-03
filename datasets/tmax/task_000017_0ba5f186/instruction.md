You are a Machine Learning Engineer preparing training data for a foundation model trained on genomic sequences. You need to validate that a newly generated synthetic dataset's GC-content distribution matches a real biological dataset after extracting the valid coding regions.

We have a set of raw biological sequences in `/home/user/data/real_sequences.fasta`. A local service serves the synthetic dataset over HTTP.

Your task is to:
1. Start the synthetic data server by running `/home/user/server.py` in the background. It will bind to `http://localhost:8080`. The synthetic sequences can be fetched via a GET request to `http://localhost:8080/synthetic`.
2. Write a script to process the real sequences from `/home/user/data/real_sequences.fasta`.
   - Find sequences that contain both the forward primer `ATGCGT` and the reverse primer `TACGCA`.
   - Extract the subsequence strictly *between* the first occurrence of the forward primer and the first subsequent occurrence of the reverse primer.
   - Calculate the GC-content (the proportion of 'G' and 'C' characters) for each extracted subsequence.
3. Fetch the synthetic sequences from the local API. Each item in the returned JSON list has a `sequence` key. Calculate the GC-content for each synthetic sequence.
4. Calculate the 1D Wasserstein distance between the GC-content distribution of the extracted real subsequences and the synthetic sequences.
5. Perform a Kernel Density Estimation (KDE) on the real subsequence GC-content data using a Gaussian kernel with a bandwidth (Scott's Rule or standard scaling, use `scipy.stats.gaussian_kde` default settings).
6. Numerically integrate this KDE (using `scipy.integrate.quad` or similar) to calculate the estimated probability mass of the real sequences having a GC-content between 0.4 and 0.6 (inclusive).
7. Save your results in a JSON file at `/home/user/results.json` with exactly the following format:
```json
{
    "extracted_real_count": <integer>,
    "wasserstein_distance": <float>,
    "kde_prob_mass_40_60": <float>
}
```
Ensure your floats are accurate to at least 4 decimal places.
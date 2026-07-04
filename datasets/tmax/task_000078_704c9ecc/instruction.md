You are an AI assistant helping a computational biology researcher run a simulated PCR experiment to compare a set of mutated genomes against a reference dataset.

The researcher has two sequence datasets:
- `/home/user/reference.fasta`
- `/home/user/mutants.fasta`

Your task is to write and execute a Python script that simulates PCR amplification on these datasets and performs a statistical hypothesis comparison to see if the mutant dataset is significantly more susceptible to amplification by a specific primer pair.

Perform the following steps:
1. Scientific Environment Management: Create a Python virtual environment at `/home/user/sim_env` and install the `scipy` package. You will use this environment to run your script.
2. Simulate PCR Amplification: Write a Python script at `/home/user/analyze_primers.py` that reads both FASTA files. 
   - Forward Primer: `ATGCGT`
   - Reverse Primer: `TACGCA`
   A sequence is considered "amplified" if it contains the forward primer and the reverse complement of the reverse primer (which is `TGCGTA`) on the same strand, such that the reverse complement sequence starts between 10 and 100 bases (inclusive) *after* the end of the forward primer sequence.
3. Statistical Analysis: Count the number of amplified and non-amplified sequences in both the reference and mutant datasets. Use `scipy.stats.fisher_exact` to compute the two-sided p-value. The contingency table should be structured as:
   `[[reference_amplified, reference_not_amplified], [mutants_amplified, mutants_not_amplified]]`
4. Output: Write the results to `/home/user/pcr_results.json` strictly in the following JSON format:
   ```json
   {
       "reference_amplified": <int>,
       "reference_total": <int>,
       "mutants_amplified": <int>,
       "mutants_total": <int>,
       "p_value": <float>
   }
   ```
   Do not round the p-value.

Please complete the script, run it using your virtual environment, and ensure the JSON file is created.
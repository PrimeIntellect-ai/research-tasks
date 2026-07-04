You are a performance engineer profiling a new MCMC-based bioinformatics pipeline. The pipeline outputs a log file containing Monte Carlo Markov Chain (MCMC) sampling iterations, sequence alignments, and fitness scores. 

Your objective is to write and execute a Bash data-processing pipeline (using standard tools like `awk`, `grep`, `sed`, `sort`, `bc`, etc.) to analyze the MCMC logs, compute a probability distribution distance metric to detect sampling bias, and extract a target sequence for primer design.

The raw log file is located at `/home/user/mcmc_results.tsv`. It is a tab-separated values file with the following columns:
1. `Iteration` (Integer)
2. `Sequence` (String of DNA characters)
3. `Score` (Integer from 0 to 100)
4. `Accepted` (1 or 0, indicating if the MCMC step was accepted)

Perform the following analysis:
1. **Burn-in Filtering:** Discard the header row and the first 500 iterations (i.e., ignore any row where `Iteration` <= 500).
2. **Rejection Filtering:** Only consider iterations where `Accepted` is `1`.
3. **Probability Distribution Distance:** 
   Group the `Score` values of the remaining valid iterations into 5 bins:
   - Bin 1: 0 <= Score < 20
   - Bin 2: 20 <= Score < 40
   - Bin 3: 40 <= Score < 60
   - Bin 4: 60 <= Score < 80
   - Bin 5: 80 <= Score <= 100
   
   Calculate the empirical probability $P_i$ for each bin ($P_i$ = count in Bin $i$ / total valid iterations).
   Compute the Total Variation Distance (TVD) between this empirical distribution and a uniform distribution ($U_i = 0.2$ for all 5 bins). 
   The formula for TVD is: $TVD = 0.5 \times \sum_{i=1}^{5} |P_i - 0.2|$.
4. **Primer Design Extraction:** Find the row with the maximum `Score` among the valid (post-burn-in, accepted) iterations. If there is a tie, select the one that occurs first in the file. Extract the first 10 characters of its `Sequence` to serve as a candidate primer.

Output your final results to a JSON file located at `/home/user/analysis_summary.json` with exactly this structure:
```json
{
  "tvd": 0.1234,
  "primer": "ACGTACGTAC"
}
```
Round the `tvd` value to exactly 4 decimal places.
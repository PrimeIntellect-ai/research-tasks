You are acting as a bioinformatics analyst. You have been given a custom C++ analysis tool that computes a specific "sequence complexity variance" metric for DNA sequences. 

However, the pipeline has some issues and is incomplete. You must fix the tool, compile it, process two datasets, and perform a statistical comparison.

Your workspace is located at `/home/user/sequence_project/`.

Here are your instructions:

1. **Fix Numerical Instability**: The source code for the tool is located at `/home/user/sequence_project/src/analyze_seqs.cpp`. The function `calculate_complexity_variance` computes the population variance of transformed nucleotide values. Currently, it uses a naive single-pass formula ($E[X^2] - E[X]^2$) which suffers from catastrophic cancellation due to the large artificial offset applied to the values, resulting in incorrect (and sometimes negative) variances. Modify the C++ code to use a numerically stable method (such as Welford's online algorithm or a stable two-pass approach) to calculate the population variance. 

2. **Compile the Tool**: Compile the fixed C++ code using `g++` (with `-O3` optimization). Save the compiled executable to `/home/user/sequence_project/bin/analyze_seqs`.

3. **Process the Datasets**: Run your compiled tool on the two provided FASTA datasets:
   - `/home/user/sequence_project/data/cohort_A.fasta`
   - `/home/user/sequence_project/data/cohort_B.fasta`
   The tool outputs CSV data to standard output in the format: `SequenceID,Variance`. Save the outputs to `cohort_A_results.csv` and `cohort_B_results.csv` in the `/home/user/sequence_project/data/` directory.

4. **Statistical Hypothesis Comparison**: Write a Python script to compare the variance distributions of the two cohorts. Read the generated CSV files and perform a two-sided Welch's t-test (independent t-test with unequal variances) comparing the sequence variances of Cohort A vs Cohort B.

5. **Generate Output**: Your Python script must output the results of the statistical test to a JSON file at `/home/user/sequence_project/results.json`. The JSON file must have exactly this structure:
```json
{
  "t_statistic": 1.234567,
  "p_value": 0.0123456
}
```
*(Note: Replace the numbers with your actual calculated float values).*

Ensure all dependencies are met and the final JSON file is correctly formatted. You may install any necessary Python packages (like `scipy` or `pandas`) if they are missing.
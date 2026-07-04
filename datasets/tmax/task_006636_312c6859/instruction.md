You are an AI assistant helping a researcher organize and analyze a dataset of scientific abstracts. 

The researcher wants to know if there is a correlation between the textual similarity of abstracts and the difference in their citation counts. Since they are working in a constrained environment without access to heavy ML models, they want you to write a Go program to perform a simplified deterministic "embedding" of the text, compute similarities, and run a statistical analysis.

Here is your task:

1. **Setup**: Initialize a Go module in `/home/user/abstract_analysis` and install any necessary mathematical packages (e.g., `gonum`). Write your Go code in `/home/user/abstract_analysis/analyze.go`.

2. **Data**: Read the dataset from `/home/user/dataset.csv`. The CSV has a header and three columns: `id`, `abstract`, and `citations`.

3. **Embedding Computation**:
   For each abstract, compute a 128-dimensional vector representing the frequency of ASCII characters.
   - Initialize a zero vector of length 128.
   - For each character in the `abstract` string, if its integer value is between 0 and 127 inclusive, increment the corresponding index in the vector.
   - Normalize the vector to unit length (L2 norm). If the L2 norm is 0, the vector remains all zeros.

4. **Pairwise Metrics**:
   - For all unique pairs of documents $(i, j)$ where $i < j$ (using the 0-based index of the rows as they appear in the CSV, ignoring the header), compute:
     a) The Cosine Similarity between their embedding vectors.
     b) The Absolute Citation Difference: $|citations_i - citations_j|$.

5. **Correlation and Confidence Interval**:
   - Compute the Pearson correlation coefficient ($r$) between the array of Cosine Similarities and the array of Absolute Citation Differences across all pairs.
   - Calculate the 95% Confidence Interval for this correlation using Fisher's z-transformation:
     - $z = 0.5 \times \ln((1+r)/(1-r))$
     - Standard Error $SE = \frac{1}{\sqrt{N - 3}}$, where $N$ is the number of *pairs*.
     - 95% CI for $z$: $[z_{lower}, z_{upper}] = [z - 1.96 \times SE, z + 1.96 \times SE]$
     - Inverse transform to get the CI for $r$: $r_{bound} = \frac{e^{2z_{bound}} - 1}{e^{2z_{bound}} + 1}$

6. **Output**:
   Write the results to `/home/user/results.json` with exactly this format (rounded to 4 decimal places):
   ```json
   {
     "correlation": 0.1234,
     "ci_lower": -0.1234,
     "ci_upper": 0.5678
   }
   ```

Run your Go program to generate the output file.
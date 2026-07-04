You are a machine learning engineer preparing a dataset for a model that predicts transcription factor binding affinities. You have been given a raw dataset of simulated DNA sequences and 1D spatial binding signals, but you need to filter the data for numerical stability, biological relevance, and extract specific mathematical features using only standard Linux shell tools.

Do not use Python, Perl, or any non-standard binaries. You must use standard Bash tools (e.g., `awk`, `grep`, `sed`, `bc`, `tr`, `coreutils`).

The raw data is located at `/home/user/raw_data.tsv`. It is a Tab-Separated Values (TSV) file with no header. The columns are:
1. `Sequence_ID`: A unique identifier for the sequence.
2. `DNA_Sequence`: A string of nucleotides (A, C, G, T).
3. `Signal_Values`: A comma-separated list of floating-point numbers representing the binding signal on a uniform 1D grid ($x = 0, 1, 2, ... N$, so $\Delta x = 1$).

You must process this file and write the results to `/home/user/training_features.tsv`. The output must be a TSV file with three columns: `Sequence_ID`, `Integral_Value`, and `TV_Distance`.

**Processing Rules & Filters:**
1. **Primer Alignment:** The `DNA_Sequence` MUST contain the exact motif "ATGC". Discard rows that do not.
2. **Biological Stability (GC Content):** The GC content of the `DNA_Sequence` (the total count of 'G' and 'C' characters divided by the sequence length) must be between `0.4` and `0.6` inclusive. Discard rows outside this range.
3. **Numerical Stability Filter:** The `Signal_Values` array must not contain "NaN" or "Inf". Discard rows that do.
4. **Numerical Differentiation Filter:** Compute the first derivative of the signal using forward finite differences: $\Delta y_i = y_{i+1} - y_i$. If the absolute value of ANY difference exceeds `50.0`, discard the row (this removes noisy outliers).

**Feature Extraction (for rows that pass all filters):**
1. **Numerical Integration:** Compute the area under the curve of the `Signal_Values` using the Trapezoidal rule. Since $\Delta x = 1$, the integral is the sum of all points minus half the first point and half the last point.
2. **Probability Distribution Distance:** Calculate the Total Variation (TV) distance of the sequence's base frequencies from a uniform distribution. 
   - First, find the frequencies $p_A, p_C, p_G, p_T$ of each nucleotide in the sequence (e.g., $p_A = \text{count}(A) / \text{length}$).
   - The uniform distribution is $q = 0.25$ for each base.
   - The TV distance is: $TV = 0.5 \times ( |p_A - 0.25| + |p_C - 0.25| + |p_G - 0.25| + |p_T - 0.25| )$

**Output Format:**
Write the valid records to `/home/user/training_features.tsv` separated by tabs. Format the `Integral_Value` and `TV_Distance` to exactly 3 decimal places (e.g., `8.000`).

Example expected output format:
```
S1	8.000	0.000
S5	7.500	0.150
```
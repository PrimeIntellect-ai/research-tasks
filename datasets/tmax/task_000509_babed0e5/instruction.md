You are a data scientist working on modeling nucleotide sequence properties. We need to analyze the local GC-content of a synthetic genomic sequence by treating the sequence as a 1-dimensional spatial domain. Because the GC-content can change abruptly, you will implement an adaptive 1D mesh (domain decomposition and refinement) and then fit a linear regression model to the spatial data.

Write a Go program (e.g., `main.go`) to perform the following steps:

1. **Parse the FASTA file**: Read the file located at `/home/user/input.fasta`. It contains a single sequence. Concatenate all lines of the sequence (ignoring the header starting with `>`) to form the complete continuous string.

2. **Initial Domain Decomposition**: Create an initial 1D mesh by dividing the sequence into equal bins of exactly 500 bases each. 

3. **Mesh Refinement**:
   - Calculate the GC-content (ratio of 'G' and 'C' bases to the total bases in the bin) for each of the initial bins.
   - For every bin $i$, calculate the absolute difference in GC-content between it and its immediate adjacent bins (left neighbor $i-1$ and right neighbor $i+1$). Bins at the sequence boundaries only have one neighbor.
   - If the absolute difference with *any* neighbor is strictly greater than `0.15`, mark this bin for refinement.
   - **Crucial**: Evaluate the refinement condition for all initial bins simultaneously (based on the initial GC-content values) *before* applying any splits.
   - For each marked bin, split it exactly in half (yielding two adjacent bins of 250 bases each). Leave unmarked bins as 500 bases.

4. **Recalculation and Curve Fitting**:
   - Recalculate the GC-content for all final bins in your refined mesh.
   - Determine the spatial midpoint $x$ for each bin. The midpoint is measured in 0-indexed base positions from the start of the sequence. For example, an un-split bin spanning from index 0 up to 500 has a midpoint of `250.0`. A split bin spanning from 1000 to 1250 has a midpoint of `1125.0`.
   - Perform an Ordinary Least Squares (OLS) linear regression $y = mx + b$ where your independent variable $x$ is the bin midpoint, and the dependent variable $y$ is the bin's GC-content.

5. **Output**:
   Write the final metrics to a JSON file at `/home/user/results.json`. The JSON must exactly match the following format (round the slope and intercept to 6 decimal places):

   ```json
   {
     "sequence_length": <total_bases>,
     "initial_bins": <count_of_initial_bins>,
     "refined_bins": <total_count_of_bins_after_refinement>,
     "slope": <m>,
     "intercept": <b>
   }
   ```

You must use Go (`go run`, `go build`, etc.) to implement and execute the analysis. Do not use external libraries for the regression or math; implement the OLS formulas natively in Go.
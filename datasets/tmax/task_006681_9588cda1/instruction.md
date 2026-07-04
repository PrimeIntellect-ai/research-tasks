You are a bioinformatics analyst tasked with processing a dataset of viral sequence abundances over time to identify and analyze the dominant evolutionary lineage. 

A dataset of viral sequence observations is located at `/home/user/data/viral_samples.csv`. It contains three columns: `Timepoint` (integer, in days), `Sequence` (string of nucleotides), and `Abundance` (float). 

Your task involves data reshaping, graph analysis, numerical calculus, and visualization. Write and execute code in the language of your choice to perform the following steps:

1. **Data Reshaping & Graph Construction**: 
   Construct a mutation network (graph) of all unique sequences found in the dataset. Two sequences are connected by an undirected edge if and only if their Hamming distance is exactly 1 (i.e., they differ by exactly one nucleotide, having the same total length).
   
2. **Lineage Identification**:
   Find the largest connected component in this mutation graph. This represents the main evolutionary lineage. If there is a tie, pick the one containing the sequence with the highest single abundance value overall.

3. **Numerical Calculus on Dominant Strain**:
   Within this largest connected component, identify the "dominant sequence"—defined as the sequence with the highest *total cumulative abundance* across all timepoints. 
   For this dominant sequence, you must calculate:
   - The definite integral of its abundance over the entire time range (from the minimum `Timepoint` to the maximum `Timepoint`) using the **Trapezoidal Rule**. Note: The timepoints are guaranteed to be uniformly spaced with $\Delta t = 1$. If a sequence is missing at a specific timepoint in the CSV, assume its abundance is 0.0 for that timepoint.
   - The rate of change (derivative) of its abundance at exactly `Timepoint = 2` using the **Central Difference** method ($f'(x) \approx \frac{f(x+1) - f(x-1)}{2}$).

4. **Output Generation**:
   Create a JSON file at `/home/user/output/analysis_results.json` with the following exact keys and format:
   ```json
   {
       "largest_component_size": <integer, number of sequences in the largest component>,
       "dominant_sequence": "<string, the nucleotide sequence>",
       "abundance_integral": <float, rounded to 2 decimal places>,
       "derivative_at_t_2": <float, rounded to 2 decimal places>
   }
   ```

5. **Data Visualization**:
   Create a plot displaying the abundance of this dominant sequence over time. Save this plot as `/home/user/output/dominant_abundance.png`. The format must be a standard image file (PNG).

You may install any required libraries (e.g., Python's `networkx`, `numpy`, `scipy`, `matplotlib`, or equivalent in your chosen language) using standard package managers. Make sure to create the output directory `/home/user/output` if it does not exist.
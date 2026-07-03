You are a bioinformatics analyst tasked with analyzing the structural flexibility of a DNA sequence using a 1D mesh refinement approach. We have raw observational data containing sequence flexibility scores, but it needs to be reshaped, and a C++ tool must be built to integrate these scores over adaptive regions.

Step 1: Observational Data Reshaping
I have placed a raw data file at `/home/user/raw_data.json`. It is a JSON array of objects, e.g., `[{"pos": 0, "val": 10.5}, {"pos": 1, "val": 10.6}, ...]`. 
Extract the data and reshape it into a space-separated text file at `/home/user/processed_scores.txt` with no header, containing just two columns: `pos` and `val`.

Step 2: C++ Tool for Adaptive Mesh Integration
Write a C++ program in `/home/user/analyze_flex.cpp` to analyze `processed_scores.txt`. Your C++ code must do the following:

1. **Initial Domain Decomposition**: Divide the 1000-position sequence (positions 0 to 999) into 10 equal initial "bins" (each containing 100 positions, e.g., 0-99, 100-199, etc.).
2. **Probability Distribution Distance Metric**: For each bin, normalize the 100 values so they sum to 1.0, creating an empirical probability distribution $P$. Calculate the Total Variation Distance (TVD) between $P$ and a uniform distribution $U$ (where $U_i = 1/100$). 
   Formula: $TVD = 0.5 \times \sum_{i=1}^{100} |P_i - U_i|$
3. **Mesh Refinement**: If the TVD for a bin is strictly greater than `0.15`, refine the mesh by splitting that bin into two equal halves (e.g., a bin of 0-99 splits into 0-49 and 50-99). Only perform a maximum of ONE refinement pass (do not recursively split).
4. **Numerical Integration**: For each final bin (whether refined or not), calculate the definite integral of the *original, unnormalized* `val` scores over the bin's domain using the Trapezoidal Rule. Note that $\Delta x = 1$. The interval for a bin from `start` to `end` has `end - start` trapezoids.
5. **Output**: Write the results to `/home/user/integrated_flexibility.log`.
   Format each line exactly as: `[start] [end] [integral_value]` (where `integral_value` is printed to 2 decimal places). Start and end are inclusive indices (e.g., `0 99 1050.50`).

Compile your code using `g++ -std=c++17` and run it to produce the log file.
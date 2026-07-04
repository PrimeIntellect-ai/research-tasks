You are a performance engineer profiling a C++ particle simulation. You noticed that compiling the simulation with aggressive floating-point optimizations (`-Ofast`) changes the reduction order, causing the final energy distributions to diverge from the reference dataset compiled with `-O0`.

Your task is to quantify this divergence by writing a C++ program that compares the two distributions using the Kullback-Leibler (KL) divergence.

You have two files containing the final energy states (one floating-point number per line):
- `/home/user/reference.txt`
- `/home/user/optimized.txt`

Write a C++ program at `/home/user/compare.cpp` that does the following:
1. Reads all floating-point values from both files.
2. Finds the global minimum (`min_val`) and global maximum (`max_val`) across **both** datasets combined.
3. Computes a 100-bin histogram for each dataset over the range `[min_val, max_val]`. 
   - The bin width is `W = (max_val - min_val) / 100.0`.
   - A value `v` belongs to bin index `floor((v - min_val) / W)`.
   - If `v == max_val`, place it in the last bin (index 99).
4. Converts the histograms into probability mass functions (PMFs), `P` for reference and `Q` for optimized, by dividing each bin's count by the total number of points in that respective dataset.
5. To avoid log(0) and division by zero, adds an epsilon of `1e-9` to each bin's probability: 
   - `P_adj[i] = P[i] + 1e-9`
   - `Q_adj[i] = Q[i] + 1e-9`
6. Computes the KL divergence: `KL = sum_{i=0}^{99} P_adj[i] * ln(P_adj[i] / Q_adj[i])` (where `ln` is the natural logarithm).
7. Writes the final KL divergence, formatted to exactly 6 decimal places, to `/home/user/kl_divergence.txt`.

Compile and run your program to produce the output file.
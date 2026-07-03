You are a performance engineer analyzing the execution time of a parallel simulation kernel across a 1D spatial domain. You need to write a C++ tool that reads profiling data, recursively decomposes the domain, measures how much the execution time distribution deviates from an ideal uniform distribution, and fits a curve to predict scaling bottlenecks.

Write a C++ program at `/home/user/profiler.cpp` and compile it to `/home/user/profiler` (using `g++ -O3 -std=c++17`). 

**Input Data:**
Assume there is a CSV file at `/home/user/profiling_data.csv` with a header `x,time`. 
- `x` is the coordinate of a particle (float, $0 \le x \le 1$).
- `time` is the execution time of the kernel for that particle (float).

**Algorithm Specifications:**
1. **Global Bounds:** Find the global minimum ($T_{min}$) and maximum ($T_{max}$) execution times across all data points in the CSV.
2. **Domain Decomposition:** You will evaluate the domain at 5 different refinement levels: $N \in \{2, 4, 8, 16, 32\}$.
   For a given $N$, decompose the domain $[0, 1)$ into $N$ equal-width sub-domains: $[0, 1/N), [1/N, 2/N), \dots, [(N-1)/N, 1.0]$. (Include exactly $1.0$ in the very last bin).
3. **Distribution Distance:** For each sub-domain at level $N$:
   - Identify all particles whose `x` coordinate falls in this sub-domain.
   - Build an empirical histogram of their `time` values using exactly 10 equally spaced bins spanning from the *global* $T_{min}$ to the *global* $T_{max}$. (Bin width is $(T_{max} - T_{min}) / 10$).
   - Normalize the histogram into a probability distribution $P$ (divide each bin count by the total number of particles in this sub-domain). If a sub-domain has 0 particles, its maximum Total Variation Distance (TVD) is defined as $1.0$.
   - The ideal distribution $Q$ is perfectly uniform ($Q_k = 0.1$ for all 10 bins).
   - Compute the Total Variation Distance (TVD) between $P$ and $Q$: $\text{TVD} = 0.5 \sum_{k=1}^{10} |P_k - Q_k|$.
4. **Max Distance Calculation:** For each $N$, find the maximum TVD among its $N$ sub-domains. Let this be $D_N$.
5. **Curve Fitting:** We hypothesize the worst-case distribution distance scales as $D_N = a \cdot N^b$.
   - Perform linear regression on the natural logarithms: $y_i = \ln(D_{N_i})$ and $x_i = \ln(N_i)$ for the 5 points.
   - Calculate the scaling exponent (slope) $b = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}$.

**Output:**
Your C++ program should write the final results to `/home/user/scaling_report.json` with exactly this format (rounded to 4 decimal places):
```json
{
  "exponent_b": -0.1234,
  "D_32": 0.5678
}
```

Write the code, compile it, and run it to produce the JSON file. Ensure you handle potential edge cases (like `x=1.0` assignment).
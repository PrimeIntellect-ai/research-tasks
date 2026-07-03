You are a performance engineer profiling a high-performance computing application. You have extracted memory latency frequency distributions for a "Baseline" and an "Optimized" configuration. 

You need to write a C++ program to process this data, compute the statistical distance between the distributions, and then visualize the results.

The raw histogram data is located at `/home/user/latency_data.txt`. It contains exactly two lines (rows), each with 1000 space-separated floating-point numbers representing frequency counts.
- Row 1: Baseline configuration (Distribution P)
- Row 2: Optimized configuration (Distribution Q)

The data represents discrete buckets with a constant width of `dx = 0.1`.

Task Steps:
1. Write a C++ program at `/home/user/compute_metrics.cpp` that does the following:
   - Reads the 2D array of data.
   - Adds a smoothing factor of `1e-9` to every element in both rows to prevent division-by-zero or log-of-zero errors.
   - Normalizes both rows so they become valid Probability Density Functions (PDFs). You MUST use the **trapezoidal rule** for numerical integration to find the total area, and then divide each element by this area. 
     *(Recall: Trapezoidal integral $I = \sum_{i=0}^{N-2} \frac{y_i + y_{i+1}}{2} dx$)*
   - Computes the Kullback-Leibler (KL) divergence $D_{KL}(P || Q)$ from the Baseline (P) to the Optimized (Q) configuration. The KL divergence integral $\int P(x) \log(P(x)/Q(x)) dx$ MUST also be computed using the **trapezoidal rule**.
   - Writes the normalized arrays to `/home/user/normalized_data.csv` (2 lines, 1000 comma-separated values per line, matching the input order).
   - Writes the computed KL divergence to `/home/user/kl_divergence.txt` in exactly this format: `KL: <value>` (round to 6 decimal places).

2. Compile and run your C++ program.

3. Write a Python script at `/home/user/plot_data.py` that reads `/home/user/normalized_data.csv` and generates a line plot comparing the two distributions. Save the plot as `/home/user/distributions.png`.

Ensure all file paths are exact and your C++ code strictly uses the trapezoidal rule for all integrations.
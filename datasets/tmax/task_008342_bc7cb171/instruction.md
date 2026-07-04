You are a machine learning engineer preparing a training dataset of sensor readings for a forecasting model. The raw observational data you received is in a messy, multi-line string format and needs to be cleaned, mathematically transformed, and statistically validated against a reference distribution. 

You must use standard Bash tools (like `awk`, `sed`, `grep`, `bash`, `bc`, etc.) to process the data.

Your tasks are as follows:

1. **Observational Data Reshaping**:
   You have a file at `/home/user/raw_data.txt` containing blocks of sensor records. 
   Extract the `timestamp` and `reading` values only for records where the `sensor` is `ALPHA`. 
   Save the extracted data to `/home/user/alpha_sensor.tsv` as a two-column tab-separated file: `timestamp` in the first column, `reading` in the second column. The file should not contain any headers, just the numerical values. The data is guaranteed to be chronologically ordered.

2. **Numerical Integration**:
   Calculate the cumulative integral of the `reading` (as a function of `timestamp`) using the **Trapezoidal Rule**. 
   The first value of the cumulative integral should be exactly `0.0` (at the first timestamp).
   Save the sequence of cumulative integral values (one per line, retaining standard floating-point precision) to `/home/user/integral.txt`.

3. **Numerical Differentiation**:
   Calculate the forward difference derivative of the `reading` with respect to `timestamp` (i.e., $\frac{v_{i+1} - v_i}{t_{i+1} - t_i}$).
   Drop the final point since a forward difference cannot be computed for it.
   Save the sequence of derivative values (one per line) to `/home/user/derivative.txt`.

4. **Scientific Software Compilation from Source**:
   There is a C source file located at `/home/user/ks_stat.c` that computes the Kolmogorov-Smirnov (KS) statistic (a probability distribution distance metric) between two sets of samples.
   Compile this C file using `gcc` into an executable named `/home/user/ks_stat`. (Standard library linking only, e.g., `-lm` if needed).

5. **Probability Distribution Distance**:
   A reference distribution of integral values is provided at `/home/user/reference.txt`.
   Run your compiled `/home/user/ks_stat` tool, passing your calculated `/home/user/integral.txt` as the first argument and `/home/user/reference.txt` as the second argument.
   The tool will output a single floating point number (the KS distance). Save this output to `/home/user/ks_result.txt`.

Ensure all output files are placed exactly at the specified paths in `/home/user`.
You are an AI assistant acting as a data scientist. We have a pipeline to fit models on network time-series data, specifically calculating the graph Fourier transform to analyze signals on a molecular network.

We need you to set up the environment and write a reproducible Bash computation pipeline to calculate bootstrap confidence intervals for the dominant spectral magnitude.

Here are your instructions:

1. **Fix and Install the Vendored Package:**
   There is a package provided at `/app/graph_tools-1.0.0`. It contains a CLI for graph spectral analysis.
   However, the installation process is currently broken due to a deliberate misconfiguration in its executable wrapper `bin/graph_tool`. You need to identify the issue, fix it, and install the package by running `make install` (which will place the executable in `/usr/local/bin/graph_tool`).

2. **Develop the Bootstrap Pipeline:**
   Write a Bash script at `/home/user/analyze.sh` that takes an input CSV file and an integer `N` for the number of bootstrap iterations as arguments:
   `bash /home/user/analyze.sh /home/user/data/signals.csv 500`

   The script must:
   - Perform `N` bootstrap iterations. In each iteration, it should sample rows from the input CSV *with replacement* to create a new CSV of the same size (excluding the header, but keeping the header in the sampled file).
   - Run the graph spectral tool on the sampled CSV: `graph_tool --input <sampled.csv>`
   - The tool outputs a single float value to standard output, representing the dominant spectral magnitude.
   - Collect these `N` values, sort them numerically, and determine the 95% confidence interval (the 2.5th percentile and 97.5th percentile values). For $N=500$, these correspond to the 13th and 488th sorted values (using 1-based indexing).
   - Output the results as a JSON file at `/home/user/results.json` with exactly this format:
     ```json
     {
       "ci_lower": 12.34,
       "ci_upper": 56.78
     }
     ```

3. **Execution:**
   - The input data will be available at `/home/user/data/signals.csv`.
   - After developing the script, run it with `N=500`.

Ensure your bash script is robust and uses standard command-line utilities (e.g., `awk`, `shuf`, `sort`). The accuracy of your confidence intervals will be evaluated programmatically against a high-iteration reference execution.
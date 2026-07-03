You are an MLOps engineer responsible for managing an automated pipeline that tracks conversion rates using Bayesian inference. The pipeline currently fails due to analysis environment issues, a broken ETL process, and a misconfigured plotting artifact generator.

Your task is to fix the pipeline and generate the correct tracking artifacts.

**Phase 1: Environment Setup**
1. Create a Python virtual environment at `/home/user/venv`.
2. Install the necessary packages to perform scientific computing and plotting (e.g., `numpy`, `scipy`, `matplotlib`, `pandas`).

**Phase 2: ETL and Bayesian Inference**
The raw data is located at `/home/user/data/conversions.csv`. It contains two columns: `id` and `clicked` (1 for click, 0 for no click).
There is a broken script at `/home/user/analyze.py`. You must fix or rewrite this script to:
1. Read and aggregate the large CSV file efficiently.
2. Perform a Bayesian update to estimate the true conversion rate. Assume a Beta distribution prior of Beta(α=1, β=1). Update this prior using the binomial data from the CSV to calculate the exact posterior parameters (α, β).
3. Compute the analytical mean and variance of this posterior distribution.
4. Output these results to `/home/user/artifacts/metrics.json` with the following exact keys:
   - `"posterior_alpha"` (integer)
   - `"posterior_beta"` (integer)
   - `"posterior_mean"` (float)
   - `"posterior_variance"` (float)

**Phase 3: Artifact Generation**
The script `/home/user/analyze.py` is also supposed to generate a plot of the posterior Probability Density Function (PDF) over the range [0, 1] and save it to `/home/user/artifacts/posterior.png`.
Currently, when the script runs in our headless CI/CD environment, it produces a completely blank plot (0 bytes or just white space) due to matplotlib backend misconfiguration and incorrect save sequences. 
Fix the code so that it produces a valid, non-blank PNG image of the plot.

Ensure the final state of the system contains:
- `/home/user/artifacts/metrics.json`
- `/home/user/artifacts/posterior.png` (a valid, non-blank image file)

You may write your code in Python and execute it directly in the terminal.
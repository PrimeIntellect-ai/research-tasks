You are a data analyst working on an A/B test for a website. Your goal is to process the raw experiment data, calculate the Bayesian probability that Variant B is better than Variant A, fix a broken plotting script, and tie it all together in a reproducible pipeline.

You have been provided with two CSV files:
1. `/home/user/data/impressions.csv` containing `date,variant,impressions`
2. `/home/user/data/conversions.csv` containing `date,variant,conversions`

Your tasks are:

1. **Data Joining & Aggregation**: Create a merged dataset that calculates the total number of impressions and total number of conversions for both Variant A and Variant B. 

2. **Bayesian Inference**: Write a script (in any language you choose, Python is recommended) to calculate the probability that the true conversion rate of Variant B is strictly greater than Variant A. 
   - Assume a Beta(1, 1) prior distribution for both variants.
   - Use a Monte Carlo simulation with exactly 1,000,000 samples to estimate this probability.
   - If using Python, set `numpy.random.seed(42)` immediately before generating the samples to ensure reproducibility. Generate Variant A's samples first, then Variant B's.
   - Save the resulting probability (rounded to 4 decimal places, e.g., `0.9521`) to `/home/user/prob_B_better.txt`.

3. **Fix the Plotting Script**: There is an existing script at `/home/user/scripts/plot_results.py` that is supposed to generate a plot of the posterior distributions. However, because it's being run in a headless Linux environment, it is producing a blank image. Fix the script so that it correctly saves the plot to `/home/user/posterior_plot.png` without requiring an interactive display backend.

4. **Reproducible Pipeline**: Create a shell script at `/home/user/run_pipeline.sh` that:
   - Sets up a local Python virtual environment in `/home/user/venv`.
   - Installs necessary dependencies (e.g., `pandas`, `scipy`, `matplotlib`).
   - Executes your data processing and Bayesian inference script.
   - Executes the fixed `/home/user/scripts/plot_results.py` script.

Ensure all outputs are placed exactly where specified. You can use standard CLI tools, Bash, and Python.
You are acting as a Machine Learning Engineer preparing a data processing pipeline on a headless Linux server. 

We have a broken pipeline in `/home/user/ml_pipeline`. The pipeline consists of a bash script (`run.sh`) that invokes a python script (`process_data.py`) to generate synthetic high-dimensional data, perform dimensionality reduction (PCA), run a hypothesis test (t-test and confidence interval) on the first principal component, and generate a scatter plot.

Currently, the pipeline has several major issues:
1. **Headless Environment Issue:** The `process_data.py` script tries to display a plot using `plt.show()`, which crashes or produces a blank plot in our headless environment.
2. **Missing Reproducibility:** The generated data and PCA projections change every time the script runs. 
3. **Incomplete Bash Orchestration:** The `run.sh` script does not properly handle inputs or capture the statistical results.

Your tasks are:
1. Ensure the necessary Python packages are installed in the existing virtual environment located at `/home/user/venv`. The pipeline requires `numpy`, `scipy`, `scikit-learn`, and `matplotlib`.
2. Modify `/home/user/ml_pipeline/process_data.py`:
   - It must accept a random seed as its first command-line argument and use it to seed `numpy`.
   - It must use an appropriate Matplotlib backend for headless environments (e.g., `Agg`) and save the figure as `/home/user/ml_pipeline/pca_plot.png` instead of calling `plt.show()`.
3. Modify `/home/user/ml_pipeline/run.sh`:
   - It must accept an integer random seed as its first argument (defaulting to 42 if none is provided).
   - It must execute `process_data.py` using the virtual environment's python, passing the seed.
   - It must capture the printed standard output of the python script (which prints the P-value and 95% Confidence Intervals) and append a row to `/home/user/ml_pipeline/summary.tsv`.
   - The `summary.tsv` file must be tab-separated with the exact columns: `Seed`, `P-Value`, `CI_Lower`, `CI_Upper`. Include the header only if the file does not already exist.

When finished, executing `/home/user/ml_pipeline/run.sh 123` multiple times should yield identical `pca_plot.png` results and append identical rows to the TSV file. Do not change the statistical math inside `process_data.py`, only the seeding, plotting mechanism, and CLI arguments.
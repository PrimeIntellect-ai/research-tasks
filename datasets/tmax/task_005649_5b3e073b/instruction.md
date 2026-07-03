I am a researcher running domain decomposition simulations. We have a pipeline that produces a list of mesh cell volumes across various sub-domains, but we've been running into non-reproducible total volume calculations due to floating-point reduction order issues when summing millions of tiny floating-point values alongside larger ones. I need you to build a robust analysis script to process this data and perform some statistical analysis.

Here is what you need to do:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/sim_env`. Activate it and install `numpy` and `scipy`. All scripts should be run using this virtual environment's Python.

2. **Data Processing**:
   Assume there is a file at `/home/user/mesh_data.csv` containing a header `domain_id,cell_volume` and thousands of rows of simulation data. 
   Write a Python script at `/home/user/analyze_mesh.py` that:
   - Reads `/home/user/mesh_data.csv`.
   - Filters the dataset to only include "refined" mesh cells, which we define strictly as having a `cell_volume < 0.05`.
   - Computes the total volume of these refined cells. To completely avoid the floating-point reduction order errors we've been seeing, you **must** use Python's `math.fsum()` for the summation.
   - Saves this total volume, rounded to 8 decimal places, to a file named `/home/user/total_volume.txt`.

3. **Statistical Analysis**:
   - In the same script, compute a 95% bootstrap confidence interval for the **mean** volume of these refined cells.
   - Use `scipy.stats.bootstrap`. You must configure it with exactly these parameters to ensure reproducibility with our lab's automated checks: `n_resamples=10000`, `vectorized=True`, `method='BCa'`, and `random_state=42`.
   - Save the confidence interval to `/home/user/bootstrap_ci.txt`. The file should contain exactly one line with the lower and upper bounds separated by a comma, rounded to 8 decimal places (format: `lower,upper`).

Run your script to produce `/home/user/total_volume.txt` and `/home/user/bootstrap_ci.txt`.
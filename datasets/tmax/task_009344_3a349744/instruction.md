You are a data scientist analyzing molecular network interactions. We have a legacy C-based engine for computing network diffusion metrics that needs to be integrated with a Python statistical analysis pipeline. 

Your objective is to compile the C core, write a Python wrapper to process multi-dimensional graph data, perform statistical hypothesis testing to compare models, and output a verifiable results file.

Here are the specific requirements:

1. **Setup & Compilation**:
   - There is a workspace at `/home/user/network_sim`.
   - Compile the C source file at `/home/user/network_sim/src/diffusion.c` into a shared library named `libdiffusion.so` in the `/home/user/network_sim/lib/` directory.

2. **Data Processing (Multi-dimensional Arrays & Graph logic)**:
   - Read the 3D NumPy array at `/home/user/network_sim/data/graphs.npy`. It has the shape `(K, N, N)`, representing `K` different adjacency matrices of size `N x N`.
   - Write a Python script (`/home/user/network_sim/analyze.py`) that uses `ctypes` to load `libdiffusion.so`.
   - The C library contains a function `double compute_diffusion(double* adj, int N)` which computes a diffusion score for a single `N x N` flattened adjacency matrix.
   - For each of the `K` graphs, call this C function from Python to compute its diffusion score. Store these `K` scores.

3. **Statistical Hypothesis Comparison**:
   - Read the binary outcomes from `/home/user/network_sim/data/outcomes.csv`. It contains a single column `outcome` of length `K`.
   - Fit two models using `statsmodels` (or `scipy`/`sklearn` if you prefer, but `statsmodels` is standard for this):
     - **Model A (Null Model)**: A logistic regression predicting `outcome` using only an intercept.
     - **Model B (Full Model)**: A logistic regression predicting `outcome` using the computed diffusion scores (and an intercept).
   - Perform a Likelihood Ratio Test (LRT) to compare Model B against Model A to see if the diffusion score significantly improves the model fit. Extract the p-value of this test.

4. **Output & Verification**:
   - Calculate the mean of the `K` diffusion scores.
   - Save the results to `/home/user/network_sim/results/summary.json` exactly in this format:
     ```json
     {
       "mean_diffusion_score": 123.456,
       "lrt_p_value": 0.0123
     }
     ```
   - (Round values to 6 decimal places).

Create any necessary directories. You have complete freedom to write the Python code as you see fit, as long as it adheres to the pipeline above and produces the final `summary.json` file.
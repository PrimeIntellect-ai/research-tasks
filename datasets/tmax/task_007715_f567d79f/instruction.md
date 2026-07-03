I am a researcher running computational fluid dynamics simulations. I have a large dataset of velocity fields over time, and I need to extract the dominant spatial modes using Proper Orthogonal Decomposition (POD). 

The raw simulation data is stored in an HDF5 file located at `/home/user/sim_data.h5`. The file contains a single dataset named `velocity_field` with shape $(T, X)$, where $T$ is the number of time steps and $X$ is the number of spatial points.

I need you to write and run a Python script to perform the following steps:
1. Set up a Python virtual environment at `/home/user/venv` and install the necessary scientific packages (`numpy`, `scipy`, `h5py`).
2. Read the `velocity_field` dataset from `/home/user/sim_data.h5`.
3. Perform Proper Orthogonal Decomposition (POD) using Singular Value Decomposition (SVD):
   - Compute the temporal mean of the velocity field (mean across the time axis, i.e., axis 0).
   - Subtract this mean from the original data to get the fluctuating field, $D'$.
   - Compute the SVD of the fluctuating field $D'$ such that $D' = U \Sigma V^T$. Ensure you use a reduced (economy) SVD to save memory.
4. Extract the top 5 singular values (from $\Sigma$) and their corresponding spatial modes (the first 5 rows of $V^T$).
5. Save these results to a new HDF5 file at `/home/user/pod_results.h5` with two datasets:
   - `singular_values` (shape: `(5,)`, containing the top 5 singular values in descending order).
   - `top_modes` (shape: `(5, X)`, containing the corresponding 5 spatial modes).
6. Create a JSON summary file at `/home/user/summary.json` containing a single dictionary with the key `"sum_top_5_singular_values"` mapped to the sum of these top 5 singular values as a standard float.

Please complete this end-to-end setup and computation.
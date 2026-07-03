You are a performance engineer analyzing a legacy compiled simulation. The simulation executable is a stripped black-box binary located at `/app/hardware_sim`. It simulates hardware performance counters for different workload configurations.

Your objective is to profile this application across multiple workloads, clean the messy output, and perform dimensionality reduction using Matrix Decomposition (SVD) to identify the primary performance bottlenecks. 

Follow these steps exactly:

1. **Data Collection & Reshaping**:
   - The binary `/app/hardware_sim` accepts a single integer argument representing the `workload_id`.
   - Run the binary for `workload_id`s from `1` to `50` inclusive. 
   - For each run, the binary outputs debug text, headers, footers, and a block of numerical data (100 rows by 10 columns of float values).
   - Use bash utilities to extract ONLY the 100 rows of numerical data from each run. 
   - Concatenate the extracted numerical data for all 50 workloads in sequential order (1 to 50) to create a single dataset of size 5000 rows by 10 columns. Save this raw concatenated data to `/home/user/raw_data.txt` (space-separated).

2. **Matrix Decomposition (SVD)**:
   - Write a Python script to load `/home/user/raw_data.txt`.
   - Standardize the 5000x10 matrix such that each of the 10 columns has a mean of 0 and a standard deviation of 1 (using sample standard deviation or population standard deviation, but be consistent; use `ddof=0` standard for ML).
   - Perform Singular Value Decomposition (SVD) on the standardized matrix.
   - Determine the minimum number of singular values, $k$, required to explain **at least 95.0%** of the total variance in the dataset.
   - Reconstruct the standardized matrix using **only** the top $k$ components.

3. **Output & Visualization**:
   - Save the $5000 \times 10$ reconstructed standardized matrix as a comma-separated values (CSV) file at `/home/user/reconstructed.csv` (no headers, no index).
   - Create a 2D scatter plot visualizing the First Principal Component (X-axis) vs the Second Principal Component (Y-axis) for the standardized data. Save this visualization to `/home/user/pca_plot.png`.

Your final evaluation will be based on the Mean Squared Error (MSE) between your `/home/user/reconstructed.csv` and a reference optimal reconstruction computed by our automated test suite. The MSE must be strictly less than `1e-4`.
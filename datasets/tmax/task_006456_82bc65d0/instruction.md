I'm working on a data pipeline to analyze server performance metrics, but my current Python script is buggy, non-reproducible, and crashes when trying to generate visualizations. 

I have a set of daily metric CSVs located in `/home/user/data/`. Each file contains the following columns: `server_id`, `cpu_usage`, `memory_usage`, `disk_io`, `network_tx`, and `network_rx`.

I have a script at `/home/user/process_and_plot.py` that is supposed to do the following:
1. Load all CSV files in `/home/user/data/`.
2. Aggregate the data by calculating the mean of each metric across all days for each `server_id`.
3. Standardize the aggregated features so each metric has a mean of 0 and variance of 1.
4. Apply Principal Component Analysis (PCA) to reduce the 5 metrics down to 2 principal components.
5. Save the resulting coordinates to `/home/user/output/pca_results.csv` with columns: `server_id`, `pc1`, `pc2`, sorted ascending by `server_id`.
6. Generate a scatter plot of `pc1` vs `pc2` and save it to `/home/user/output/pca_plot.png`.

However, the script has several issues:
- It fails to standardize the features before applying PCA.
- The PCA outputs slightly different results on different runs (it needs to be deterministic, please configure PCA to use `svd_solver='full'` and `random_state=42`).
- The script crashes with a display error because it's running in a headless environment and Matplotlib is trying to open an interactive window.

Please fix `/home/user/process_and_plot.py` so that it successfully performs all 6 steps, is perfectly reproducible, and correctly outputs both the CSV and the PNG to `/home/user/output/` without crashing.

You may run the script to test your fixes. Ensure `/home/user/output/` exists.
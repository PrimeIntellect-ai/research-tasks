You are assisting a researcher who is running simulations of spectroscopic data. A recent batch of simulations generated an output file containing observational data, but a bug in the simulation code introduced near-singular artifacts: some sensor channels (columns) are completely dead (producing constant zero values), and some channels are exactly duplicated (perfectly collinear).

This collinearity causes our downstream matrix factorization and statistical analysis tools to fail. 

Your task is to build a data cleaning and analysis pipeline to extract the principal components of the signal. You must do the following:

1. **Read the Data:** Read the dataset named `spectra` from the HDF5 file located at `/home/user/sim_data.h5`. The data is a 2D array where rows are observations (samples) and columns are wavelength channels.
2. **Reshape and Filter (Data Cleaning):**
    - Identify and remove any columns that have a standard deviation of exactly 0 (dead channels).
    - Identify any identical (duplicated) columns. For any set of exactly identical columns, keep only the *first* one (the one with the lowest original column index) and remove the duplicates.
3. **Statistical Analysis:** 
    - Perform Singular Value Decomposition (SVD) on the cleaned matrix.
    - Extract the top 3 largest singular values.
4. **Output:** Write the top 3 singular values to a file named `/home/user/top_singular_values.csv`. 
    - The file should contain a single line with the 3 values separated by commas.
    - Each value must be rounded to exactly 4 decimal places.
    - The values must be sorted in descending order.

You may write your pipeline using Python, bash, or a combination of both. You are working in a standard Linux environment where `python3`, `numpy`, and `h5py` are available.

Complete the task and ensure the output file exists with the exact requested format.
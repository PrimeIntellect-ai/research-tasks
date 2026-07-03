I am a researcher running signal processing simulations, but my pipeline is currently crashing. 

I have a Jupyter notebook located at `/home/user/simulation.ipynb`. It simulates 50 noisy time-series signals, uses FFT to filter out high-frequency noise, calculates the covariance matrix `C` of the filtered signals, and finally performs a Cholesky decomposition on `C`.

However, because the FFT filtering severely reduces the rank of the data, the covariance matrix becomes singular, causing `np.linalg.cholesky(C)` to fail with a `LinAlgError`.

Your task is to fix and run the simulation:
1. Modify `/home/user/simulation.ipynb` to add a Tikhonov regularization term: add `1e-5 * np.eye(C.shape[0])` to `C` right before (or inside) the Cholesky decomposition call. You can use standard CLI tools (`sed`, `jq`, `awk`) or write a short Python script to modify the notebook file. Do not alter the random seed or other data generation steps.
2. Execute the modified notebook in-place from the terminal. 
3. To mimic our production cluster's constraints, you **must** run the notebook execution step with the environment variable `OMP_NUM_THREADS=2` explicitly set.
4. The final cell of the notebook writes the trace of the resulting Cholesky lower-triangle matrix to `/home/user/trace.txt`. Make sure this file is generated successfully.

Do not manually open a Jupyter server—do everything via the terminal (e.g., using `jupyter nbconvert`).
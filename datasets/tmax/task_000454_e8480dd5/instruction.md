You are acting as an AI assistant to a Machine Learning Engineer preparing a dataset.

We are trying to run Non-Negative Matrix Factorization (NMF) on a dataset of spectroscopic signals, but the factorization keeps failing because the input matrix is near-singular. This is caused by massive, varying baseline drifts across different observations. 

To fix this, we need to extract robust features from the data by reshaping it, analyzing the signal derivative, and integrating over specific spectral bands.

The raw data is located at `/home/user/raw_spectra.csv`. 
Each row represents one observation. The columns are:
- `obs_id`: A unique string identifier.
- `wv_400`, `wv_410`, `wv_420`, ..., `wv_800`: The signal intensity at wavelengths from 400nm to 800nm (in steps of 10nm).

Your task is to create and execute a Jupyter Notebook at `/home/user/process_spectra.ipynb` that performs the following steps:
1. Load `/home/user/raw_spectra.csv`.
2. For each observation, isolate the spectral signal (the `wv_*` columns) and compute its first derivative with respect to wavelength using finite differences (e.g., `numpy.gradient`). The spacing between points is 10nm.
3. Compute the numerical integral of the **absolute value** of the first derivative (using the trapezoidal rule, e.g., `numpy.trapz` or `scipy.integrate.trapezoid` with `dx=10`) over four distinct bands:
   - Band 1: 400nm to 490nm (inclusive)
   - Band 2: 500nm to 590nm (inclusive)
   - Band 3: 600nm to 690nm (inclusive)
   - Band 4: 700nm to 800nm (inclusive)
4. Save the resulting features to a CSV file at `/home/user/band_features.csv`. The CSV must contain exactly 5 columns: `obs_id`, `band_1`, `band_2`, `band_3`, `band_4`.

Requirements:
- You must create the pipeline in a Jupyter Notebook (`/home/user/process_spectra.ipynb`).
- You must execute the notebook programmatically (e.g., using `jupyter nbconvert --to notebook --execute` or `papermill`) so that it generates `/home/user/band_features.csv`.
- Ensure you install any necessary Python packages (like `pandas`, `numpy`, `scipy`, `jupyter`, `nbconvert`) before running.
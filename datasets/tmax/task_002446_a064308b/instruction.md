You are an AI assistant helping a scientific researcher run simulations on spectroscopy data. 

The researcher has an experimental dataset of an observed spectral doublet located at `/home/user/data/spectrum.csv`. This CSV file contains two columns: `wavelength` and `intensity`.

They have provided a custom, proprietary package used for simulating these spectral signals called `spectrosim`, located at `/app/spectrosim`. The package is written in C with a Python wrapper to optimize array manipulation and simulation speed. 

However, the package is currently broken. The researcher reported that running `make` inside `/app/spectrosim` fails to produce a working shared library because the C extension fails to load at runtime when imported into Python. 

Your task is to:
1. Identify and fix the build issue in `/app/spectrosim/Makefile`. Compile the package successfully so that `import spectrosim` works in Python. You can verify it by running `pytest /app/spectrosim/tests/`.
2. Write a Python script at `/home/user/fit_spectrum.py` that:
   - Loads the experimental dataset.
   - Uses the fixed `spectrosim.simulate(wavelengths, A1, mu1, sigma1, A2, mu2, sigma2)` function to generate synthetic signals.
   - Uses a non-linear optimization routine (e.g., from `scipy.optimize`) to fit the simulated signal to the observed `intensity` data by optimizing the 6 parameters (`A1, mu1, sigma1, A2, mu2, sigma2`).
3. Save the final optimized parameters as a JSON file at `/home/user/solution.json`. The JSON file must be a simple dictionary with exactly these keys: `"A1", "mu1", "sigma1", "A2", "mu2", "sigma2"`.

The quality of your fit will be automatically evaluated by computing the Mean Squared Error (MSE) between the experimental intensities and the intensities simulated using your provided parameters. You must achieve a highly accurate fit.
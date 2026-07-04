You are a data scientist analyzing synthetic Raman spectroscopy data. You need to fit a multi-peak model to a noisy signal, but the environment and tools require some troubleshooting.

Here is your workflow:

1. **Environment Setup**: 
   We have vendored the source code for the `lmfit` package (version 1.2.2) in `/app/lmfit-1.2.2`. However, a previous developer sabotaged its dependency requirements, causing standard installation to fail on modern Python environments. 
   - Identify the perturbation in the package's setup files (specifically looking at the `numpy` version requirement) and fix it.
   - Install the patched package into your Python environment.

2. **Spectroscopy Data Processing**:
   - You are provided a dataset at `/home/user/data/spectra.csv`. It contains two columns: `wavelength` and `intensity`. This data represents a noisy spectral signal comprising exactly three Gaussian peaks and a flat baseline.

3. **Notebook-Based Workflow Orchestration**:
   - Create a Jupyter Notebook named `/home/user/fit_spectra.ipynb`.
   - In the notebook, use the newly installed `lmfit` package to define a composite model consisting of three `GaussianModel` components and one `ConstantModel` (for the baseline).
   - Fit this composite model to the `intensity` data from the CSV.

4. **Analytical Validation & Output**:
   - Evaluate your fitted model to generate the best-fit intensity values across the same `wavelength` grid.
   - To treat the spectrum as a probability distribution for downstream distance metrics, normalize the fitted intensity array so that it sums to exactly 1.0.
   - Save this normalized 1D numpy array of fitted intensities to `/home/user/fitted_y.npy` using `numpy.save`.

To succeed, your fit must be highly accurate. An automated verifier will load your `/home/user/fitted_y.npy` and calculate the Wasserstein distance (Earth Mover's Distance) between your normalized fitted signal and the true, noiseless analytical distribution.
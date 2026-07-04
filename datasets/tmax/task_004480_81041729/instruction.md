You are a data scientist tasked with fitting models to noisy spectroscopy data and evaluating the fit quality using probability distribution distance metrics. We have a notebook-based workflow in mind, but for this task, you will orchestrate the data processing pipeline via a Python script.

We have provided a custom package called `spec_smooth` vendored at `/app/spec_smooth` that contains optimized routines for spectroscopic signal smoothing (e.g., using Savitzky-Golay filters). However, a colleague accidentally broke the package during a recent refactor, and it currently fails to install or run.

Your objectives:
1. Navigate to `/app/spec_smooth`, identify the bug (a deliberate syntax or import error), fix it, and install the package into your Python environment.
2. Write a Python script (e.g., `/home/user/process_spectra.py`) that loads two NumPy arrays:
   - `/app/data/noisy_spectra.npy` (containing raw, noisy signal data of shape `(N, M)`)
   - `/app/data/theoretical_spectra.npy` (containing the theoretical noise-free probability distributions of shape `(N, M)`)
3. Iterate over the `N` noisy spectra. For each spectrum, apply the `spec_smooth.smooth(signal, window_length=15, polyorder=3)` function to denoise it.
4. Normalize both the smoothed spectrum and the corresponding theoretical spectrum so they sum to 1 (treating them as probability distributions).
5. Compute the 1D Wasserstein distance between the normalized smoothed spectrum and the normalized theoretical spectrum for all `N` pairs using `scipy.stats.wasserstein_distance`.
6. Calculate the mean of these `N` Wasserstein distances.
7. Save this mean distance as a raw float string (e.g., `0.001234`) in the file `/home/user/mean_distance.txt`.

Your goal is to successfully recover the signal and achieve a low average Wasserstein distance. Ensure that your output file contains exactly the computed mean distance and nothing else.
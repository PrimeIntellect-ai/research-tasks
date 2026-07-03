I need your help to analyze some acoustic sensor data as part of our machinery health monitoring project. We have recorded an audio file from a newly installed turbine, located at `/app/turbine_audio.wav`. 

Your task as our data scientist is to perform spectral analysis on this audio, fit a theoretical noise model to its frequency spectrum, calculate how far the empirical spectrum deviates from an expected probability distribution, and save the results in a structured scientific format.

Please follow these exact steps:
1. **Audio Processing**: Load `/app/turbine_audio.wav`. Calculate its Power Spectral Density (PSD) using Welch's method (use a Hann window, segment length of 1024 samples, and 50% overlap).
2. **Curve Fitting**: We model the underlying continuous spectrum (ignoring sharp peaks for now) with an exponential decay model: `P(f) = A * exp(-B * f) + C`, where `f` is frequency in Hz, and `P(f)` is the PSD. Fit this curve to the calculated PSD to find the optimal parameters `A`, `B`, and `C` using least squares regression.
3. **Probability Distribution Distance**: Normalize both the empirical PSD and the fitted curve `P(f)` so that they each sum to 1 over the computed frequency bins (treating them as discrete probability distributions). Calculate the Kullback-Leibler (KL) divergence from the empirical distribution (true) to the fitted distribution (approximate). To avoid log(0) issues, add a small epsilon (1e-10) to both distributions before computing the KL divergence.
4. **Data I/O**: Create an HDF5 file named `/home/user/analysis_results.h5`. Within this file, create a group named `model_fit`. Inside this group, save the following datasets:
   - `parameters`: A 1D array containing the fitted parameters `[A, B, C]`.
   - `kl_divergence`: A scalar dataset containing the computed KL divergence.

Ensure your Python environment has the necessary libraries (like `scipy`, `numpy`, `h5py`). You will need to install them if they are missing. The evaluation script will check your output file `/home/user/analysis_results.h5` against a reference solution.
You are an AI assistant helping a data scientist with a spectral analysis and density estimation pipeline.

I have a noisy periodic signal stored in an HDF5 file at `/home/user/data/signal.h5` under the dataset name `raw_signal`. The signal was sampled at a frequency of $f_s = 1000$ Hz for 1 second (1000 samples). 

I need you to write and execute a Python script `/home/user/analyze.py` that does the following:

1. **Spectral Filtering**: Read the `raw_signal`. Perform a Discrete Fourier Transform (using `numpy.fft` or `scipy.fft`). Create a low-pass filter by zeroing out all Fourier coefficients corresponding to frequencies strictly greater than 50 Hz in absolute value. Perform an inverse FFT to obtain the `smoothed_signal`. Retain only the real part of the result.
2. **Density Estimation**: Calculate the residual noise (`raw_signal - smoothed_signal`). Fit a normal distribution to this residual noise using `scipy.stats.norm.fit` to estimate the mean ($\mu$) and standard deviation ($\sigma$).
3. **Numerical Stability Testing**: To ensure the filtering and fitting pipeline is numerically stable, generate 50 perturbed versions of the `raw_signal`. 
   - Initialize a random number generator exactly once using `np.random.seed(42)`.
   - Generate an array of uniform noise in the range $[-10^{-6}, 10^{-6}]$ of shape `(50, 1000)`.
   - Add each row to the original `raw_signal` to create 50 perturbed signals.
   - For each perturbed signal, repeat the filtering (low-pass at 50 Hz) and normal fitting to obtain 50 $\sigma$ estimates.
   - Calculate the population standard deviation (`ddof=0`) of these 50 $\sigma$ estimates. Call this `stability_std`.
4. **Data Output**: Save the results into a new HDF5 file at `/home/user/results/output.h5` with the following datasets:
   - `smoothed_signal`: 1D array of the smoothed signal from step 1.
   - `noise_params`: 1D array of shape `(2,)` containing `[\mu, \sigma]` from step 2.
   - `stability_std`: A scalar float dataset containing the standard deviation from step 3.

Make sure to install any required packages such as `h5py` or `scipy` if they are not already installed. Create the `/home/user/results` directory if it doesn't exist.
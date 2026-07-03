You are tasked with analyzing a complex acoustic signal containing overlapping, decaying resonance modes. The signal is provided as a 16-bit PCM WAV file at `/app/signal.wav` (sample rate 8000 Hz, 1-second duration). Due to the physical properties of the system, the two dominant frequencies are very close to each other, creating an ill-conditioned, near-singular optimization landscape when fitting a model.

Your objective is to write a C++ program that reads the audio data, estimates the parameters of a 2-component damped oscillator model, and performs statistical validation of the fit. 

The theoretical model for the signal is:
S(t) = A_1 * exp(-alpha_1 * t) * sin(2 * pi * f_1 * t) + A_2 * exp(-alpha_2 * t) * sin(2 * pi * f_2 * t)
where `t` is the time in seconds.

Your C++ pipeline must perform the following:
1. **Data Ingestion:** Read the audio samples from `/app/signal.wav`. You may use libraries like `libsndfile` or invoke a pre-processing script to convert it.
2. **Optimization:** Implement an optimization routine (e.g., gradient descent, Nelder-Mead, or use an external library like Ceres/dlib) to find the parameters `A1, A2, alpha1, alpha2, f1, f2` that minimize the Mean Squared Error (MSE) against the signal.
3. **Statistical Hypothesis Comparison:** Fit a 1-component model as a baseline. Calculate the F-statistic to compare the 1-component model against the 2-component model to justify that the second component is statistically significant.
4. **Monte Carlo Simulation:** Perform a Monte Carlo bootstrap by resampling the residuals of your 2-component fit at least 100 times to estimate the standard deviation of `f1` and `f2`.
5. **Scientific Data I/O:** Write the final estimated parameters and statistics to an HDF5 file at `/home/user/model_results.h5`. 

The HDF5 file must contain the following float (H5T_NATIVE_DOUBLE or H5T_NATIVE_FLOAT) datasets at the root group:
- `/f1` : Frequency of component 1 (Hz)
- `/f2` : Frequency of component 2 (Hz)
- `/A1` : Amplitude of component 1
- `/A2` : Amplitude of component 2
- `/alpha1` : Decay rate of component 1
- `/alpha2` : Decay rate of component 2
- `/f1_std` : Bootstrap standard deviation of f1
- `/f2_std` : Bootstrap standard deviation of f2
- `/F_stat` : The F-statistic comparing the 1-component and 2-component models

Constraints & Notes:
- You may install any necessary C++ libraries (e.g., `libhdf5-dev`, `libsndfile1-dev`) using `apt-get`.
- Ensure your C++ program compiles and runs successfully.
- Your solution will be evaluated by reconstructing the noiseless signal using your `/A1`, `/A2`, `/alpha1`, `/alpha2`, `/f1`, `/f2` HDF5 outputs and comparing it to the hidden ground-truth noiseless signal. The metric is the Mean Squared Error (MSE) of the reconstruction. 
- You must achieve an MSE < 0.05.
You are a data scientist analyzing acoustic resonances. We have a noisy audio recording of a physical chime being struck, located at `/app/chime_recording.wav`. The chime's acoustic signature can be modeled as a sum of three decaying sinusoidal components:

S(t) = Σ (for i=1,2,3) [ A_i * exp(-λ_i * t) * sin(2 * π * f_i * t + φ_i) ]

Your objective is to fit this model to the observational audio data, estimate the posterior distributions of the parameters, and synthesize a clean reconstructed audio file.

Perform the following steps:
1. Observational Data Reshaping: Read the audio file `/app/chime_recording.wav`. Normalize the waveform to the [-1.0, 1.0] range. Extract the sample rate and time vector (t). 
2. Optimization & MCMC: Write a Python script to estimate the parameters (A, λ, f, φ for each of the 3 components). You must implement a parallelized MCMC sampler (e.g., using `multiprocessing` or `mpi4py` to run at least 4 parallel chains) to sample the posterior distributions of these 12 parameters. Use an appropriate likelihood function based on the Mean Squared Error (MSE) between the model S(t) and the normalized audio data.
3. Visualization: Create a grid plot of the posterior distributions (histograms or KDEs) for all 12 parameters and save it as `/home/user/posteriors.png`.
4. Reconstruction: Calculate the mean of the posterior samples for each parameter. Use these mean values to generate a reconstructed acoustic signal using the model formula. Save this signal as a standard 16-bit PCM WAV file at `/home/user/reconstructed.wav` with the same sample rate as the original.
5. Parameter Log: Save the mean values of the parameters to `/home/user/parameters.csv` with columns `component,amplitude,decay,frequency,phase`.

The primary success metric is the accuracy of your reconstruction. The Mean Squared Error (MSE) between the normalized `/app/chime_recording.wav` and the normalized `/home/user/reconstructed.wav` must be highly minimized.
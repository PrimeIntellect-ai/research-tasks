You are a machine learning engineer preparing audio training data for a specialized acoustic model. The data collection sensors have captured a target acoustic signature, but it is heavily corrupted by two strong interference sources and near-singular correlated noise.

You are provided with the raw recording at `/app/sensor_data.wav` (16000 Hz sample rate). 

Your task is to isolate the target signal using matrix decomposition and probability distribution metrics, based on the analytical properties of the target signal. 

Follow these exact steps to ensure the output aligns with our data ingestion pipeline:
1. Compute the Short-Time Fourier Transform (STFT) of the audio. Use `n_fft=1024`, `hop_length=256`, and a Hann window.
2. Extract the magnitude matrix $M$ from the STFT.
3. Perform Singular Value Decomposition (SVD) on the magnitude matrix $M$. Note: Due to redundant sensor frames, the matrix may be poorly conditioned or near-singular.
4. Isolate the top 3 principal components (the components with the 3 largest singular values).
5. For each of these 3 components, its frequency profile is represented by the absolute value of its corresponding left singular vector (a column of $U$). Normalize this absolute vector so it sums to 1, treating it as an empirical probability distribution over the STFT frequency bins.
6. The target signal analytically follows a Gaussian frequency magnitude profile: $P(f) \propto \exp\left(-\frac{(f - 1000)^2}{2 \times 150^2}\right)$, where $f$ is the frequency in Hz. Compute this analytical distribution over the same frequency bins (0 to Nyquist) and normalize it to sum to 1.
7. Use the 1D Wasserstein distance (Earth Mover's Distance) to compare each of the 3 empirical distributions to the analytical distribution. The frequency bin centers (in Hz) should be used as the domain values, and the normalized profiles as the weights.
8. Identify the single component that minimizes the Wasserstein distance to the analytical target.
9. Reconstruct the magnitude spectrogram using *only* this single selected component ($M_{clean} = U_i \Sigma_{ii} V_i^T$).
10. Recombine $M_{clean}$ with the *original* phase from the initial STFT to produce a complex STFT matrix.
11. Perform the Inverse STFT to generate the time-domain waveform.
12. Save the isolated waveform as a 16-bit PCM WAV file at `/home/user/clean_training_data.wav` (ensure it remains at 16000 Hz).

Work carefully. The verification suite will compare your extracted audio directly against a pure ground-truth reference using a strict Mean Squared Error (MSE) metric threshold.
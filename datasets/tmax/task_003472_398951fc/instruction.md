You are acting as a research assistant for a materials science laboratory. We are running acoustic emission simulations to detect micro-fractures in composite materials under stress. 

We have recorded an acoustic sensor output during a recent simulation. The file is located at `/app/stress_test.wav`. Unfortunately, the recording is heavily contaminated with broadband machine noise. The actual micro-fracture events are transient acoustic bursts that occur in a specific, narrow frequency band.

Your task is to build a data processing pipeline in Rust to analyze this audio signal, identify the signal band statistically, filter out the noise, and export the scientific data.

Perform the following steps:
1. **Environment Setup**: Create a new Rust project at `/home/user/acoustic_analysis`. You will likely need system libraries for scientific data formats (e.g., HDF5). Install any necessary Ubuntu packages before building your Rust project.
2. **Signal Processing (STFT)**: Write a Rust program that reads `/app/stress_test.wav` (it is a standard 16-bit PCM WAV). Perform a Short-Time Fourier Transform (STFT) using a window size of 1024 samples, a hop size of 256 samples, and a Hann window.
3. **Statistical Analysis**: Compute the standard deviation of the magnitude for each frequency bin across all time frames. The transient micro-fractures cause high variance. Find the contiguous frequency band of exactly 50 frequency bins that has the highest average standard deviation.
4. **Spectral Filtering**: Create a mask that retains the STFT complex bins only within this 50-bin band (inclusive). Zero out all other frequency bins to remove the out-of-band noise.
5. **Reconstruction**: Perform an Inverse STFT to reconstruct the filtered time-domain audio signal. Save this as `/home/user/cleaned.wav` using the same sample rate and format as the input.
6. **Scientific Export**: Save the original, unfiltered STFT magnitude spectrogram (as a 2D array of 64-bit floats, shape: `[time_frames, frequency_bins]`) and the 1D standard deviation vector (`[frequency_bins]`) into an HDF5 file at `/home/user/analysis.h5`. Name the datasets `spectrogram` and `std_dev` respectively.

Ensure your code compiles and runs successfully, producing both `/home/user/cleaned.wav` and `/home/user/analysis.h5`. The quality of your denoising will be evaluated against a clean ground-truth reference using Mean Squared Error (MSE).
You are an ML engineer preparing training data for a novel basecalling model that translates raw DNA nanopore sequencer signals (stored as 1D audio WAV files) into genomic sequences. 

Your task is to build a reproducible, automated data preparation pipeline that processes these signals, extracts multi-dimensional features, and aligns candidate sequences. 

Perform the following steps:

1. **Signal Denoising (Array Manipulation & Audio Processing):**
   The raw nanopore sequencer current data is stored as a standard 16-bit PCM WAV file at `/app/audio/raw_squiggle.wav` (Sample rate: 8000 Hz). It has high-frequency noise.
   - Implement a 4th-order low-pass Butterworth filter with a cutoff frequency of 1500 Hz.
   - Apply this filter to the raw audio data (using zero-phase filtering, e.g., `scipy.signal.filtfilt`).
   - Save the cleaned 1D array back as a 16-bit PCM WAV file to `/home/user/clean_squiggle.wav`.

2. **Feature Extraction (Parallel Computing & Multi-dimensional Arrays):**
   - Compute the Short-Time Fourier Transform (STFT) of the cleaned signal. Use a window size (nperseg) of 256 and an overlap (noverlap) of 128.
   - Extract the magnitude (absolute value) of the STFT, creating a 2D feature matrix (Frequency Bins x Time Frames).
   - Save this 2D matrix as a NumPy binary file at `/home/user/features.npy`. 
   - *Requirement:* Ensure your feature extraction script is designed to run computations in parallel (e.g., using `multiprocessing` to process chunks of the signal, though here you'll just process the single file).

3. **Primer Sequence Alignment:**
   A preliminary basecaller has predicted a short primer sequence from the audio, located at `/app/data/candidate.txt`. The reference genome sequence is at `/app/data/reference.fasta`.
   - Implement a Smith-Waterman local sequence alignment algorithm. 
   - Scoring parameters: Match = +3, Mismatch = -1, Gap penalty = -2 (linear gap penalty).
   - Find the best local alignment score and the 0-indexed start position of this alignment on the *reference sequence*. 
   - Write the 0-indexed start position (an integer) to `/home/user/alignment_pos.txt`.

4. **Experimental Data Visualization:**
   - Generate a heatmap plot of the STFT magnitude matrix (`features.npy`).
   - Save the plot as a PNG file to `/home/user/spectrogram_plot.png`.

Ensure your final outputs are precisely named and placed in `/home/user/`. Your denoised audio will be evaluated against a hidden clean reference signal using Mean Squared Error (MSE).
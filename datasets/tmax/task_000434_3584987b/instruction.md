You are an AI assistant helping a researcher analyze simulated spectroscopic time-domain signals. 

The researcher needs a Python script `/home/user/process_signal.py` that generates a synthetic Free Induction Decay (FID) signal, processes it using Fourier transforms, validates the extracted spectral peaks against the theoretical analytical solution, and generates a visualization.

Here are the requirements for the script:
1. **Time Domain Generation:**
   - Sampling rate (`Fs`) = 1000 Hz.
   - Duration = 1 second (so time array `t` goes from 0 to 0.999 seconds, i.e., 1000 points).
   - The signal $S(t)$ is composed of 3 damped sinusoids:
     $S(t) = \sum_{i=1}^{3} A_i \exp(-t / \tau_i) \cos(2 \pi f_i t)$
   - Parameters:
     - Component 1: $A_1 = 1.0$, $\tau_1 = 0.1$ s, $f_1 = 50$ Hz
     - Component 2: $A_2 = 0.8$, $\tau_2 = 0.2$ s, $f_2 = 120$ Hz
     - Component 3: $A_3 = 0.5$, $\tau_3 = 0.05$ s, $f_3 = 200$ Hz
   - Add zero-mean Gaussian noise to the final signal with a standard deviation of 0.05. Set the numpy random seed to `42` before generating the noise.

2. **Spectral Analysis:**
   - Compute the Fast Fourier Transform (FFT) of the noisy signal.
   - Calculate the one-sided magnitude spectrum (from 0 to Nyquist frequency, inclusive if applicable, or up to Fs/2). Normalize the magnitude properly.
   - Identify the frequencies corresponding to the 3 highest peaks in the magnitude spectrum.

3. **Validation and Output:**
   - The script must write the three detected peak frequencies (sorted in ascending order) and the frequency with the absolute maximum amplitude to a file `/home/user/spectral_results.json`.
   - The JSON should have the exact following schema:
     ```json
     {
       "detected_frequencies": [f_a, f_b, f_c],
       "max_amplitude_frequency": f_max
     }
     ```
   - Generate a plot named `/home/user/spectroscopy_analysis.png` with two subplots (arranged vertically):
     - Top subplot: The noisy time-domain signal vs. time.
     - Bottom subplot: The magnitude spectrum vs. frequency (only plot 0 to 500 Hz).

Write and execute this Python script. Make sure `numpy`, `scipy`, and `matplotlib` are used correctly.
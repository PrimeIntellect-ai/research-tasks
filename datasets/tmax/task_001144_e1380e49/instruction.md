You are a data scientist modeling the acoustic resonance of a newly designed mechanical cavity. We have recorded the cavity's impulse response using a high-fidelity microphone. The recording is located at `/app/acoustic_test.wav`.

Your objective is to extract the frequency-domain properties of this signal, fit a theoretical nonlinear resonance model to the data, and integrate the theoretical energy within a specific frequency band.

Please perform the following workflow:

1. **Signal Processing**: Read the audio file `/app/acoustic_test.wav`. Compute its Power Spectral Density (PSD) using Welch's method. You must use `scipy.signal.welch` with the default Hanning window, `nperseg=4096`, and `noverlap=2048`.

2. **Nonlinear Model Fitting**: The mechanical system is known to have exactly 3 primary resonant modes within the 0 to 2000 Hz range. Isolate your empirical PSD data to the frequency range $0 \le f \le 2000$ Hz. Fit this truncated data to the following theoretical multi-Lorentzian model:
   $$ M(f) = c + \sum_{i=1}^3 \frac{a_i}{(f - f_i)^2 + w_i^2} $$
   where $c$ is a constant noise floor baseline, and for each mode $i \in \{1, 2, 3\}$, $a_i$ is the amplitude coefficient, $f_i$ is the resonant center frequency, and $w_i$ is the width parameter (damping). 

3. **Numerical Integration**: Using the parameters ($c, a_i, f_i, w_i$) you obtained from your optimal fit, calculate the definite integral of the theoretical model $M(f)$ from $f = 0$ to $f = 2000$ Hz. You may do this analytically or via high-precision numerical integration (e.g., `scipy.integrate.quad`).

4. **Output Generation**: Create a JSON file at `/home/user/resonance_results.json` containing the sorted center frequencies and the total integrated energy. The file must have exactly this structure:
   ```json
   {
       "f1": 400.12,
       "f2": 800.34,
       "f3": 1200.56,
       "total_energy_integral": 12345.67
   }
   ```
   *(Note: Ensure $f_1 < f_2 < f_3$. The values above are just examples).*

You will need to install any necessary Python packages (like `scipy`, `numpy`) in your environment to complete this task. Focus on minimizing the residual error in your curve fitting to get an accurate energy integral.
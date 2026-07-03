I am a performance engineer profiling a new HPC rack, and I need your help to configure the cooling system's optimal fan RPM based on acoustic profiling and thermal simulations.

Here is your workflow:

1. **Acoustic Transcription (Audio Fixture)**
There is an audio file located at `/app/hpc_ambient.wav`. It contains a voice recording from the lead engineer stating the absolute thermal limit in degrees Celsius, mixed with some background fan noise. Extract the spoken numerical value (an integer) from this audio file. Let this value be $T_{max}$.

2. **Acoustic Profiling (FFT)**
The background noise in `/app/hpc_ambient.wav` contains a continuous low-frequency hum from the default fan speed. Read the audio file into a NumPy array and use a Fast Fourier Transform (FFT) to determine the dominant frequency (the frequency with the highest amplitude, ignoring the 0 Hz DC offset) of the entire file. Let this integer frequency be $F_{dom}$ in Hz.

3. **Monte Carlo Thermal Simulation & Optimization**
Write a Python script parallelized using `multiprocessing` or `mpi4py` to run a Monte Carlo simulation. 
We want to find the optimal Fan RPM $R$ (where $1000 \le R \le 5000$).
For a given RPM $R$, the server temperature $T$ follows a Normal distribution:
$T \sim \mathcal{N}(\mu=95 - \frac{R}{100}, \sigma^2=5^2)$
Simulate 100,000 temperature samples for candidate RPMs (in steps of 100, i.e., 1000, 1100, ..., 5000) distributed across multiple cores.

For each RPM, calculate the empirical distribution of $T$. 
Filter out any RPM where the 95th percentile of the simulated temperatures exceeds $T_{max}$.
Out of the remaining valid RPMs, choose the optimal RPM $R_{opt}$ that minimizes the 1D Wasserstein distance between the simulated temperature distribution and a target normal distribution $\mathcal{N}(\mu=F_{dom}/2, \sigma^2=2^2)$.

4. **Service Configuration**
Write and run a Python HTTP server (e.g., using Flask, FastAPI, or `http.server`) listening on `127.0.0.1:8000`.
It must expose a GET endpoint at `/profile` that returns a JSON response exactly matching this schema:
```json
{
  "thermal_limit": <T_max>,
  "dominant_freq_hz": <F_dom>,
  "optimal_rpm": <R_opt>
}
```

Ensure the server is running as a background process or within a persistent terminal session so it can be queried.
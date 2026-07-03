You are a performance engineer tasked with profiling a distributed microservice. You have been given raw CPU power fluctuation logs and a trace of execution latencies, both of which require advanced analysis to determine system bottlenecks and stability.

Your environment is an Ubuntu Linux terminal. You have Python 3 installed, but you may need to install additional scientific libraries (like `numpy` and `scipy`).

**Available Data:**
1. `/home/user/cpu_signal.csv`: Contains CPU power consumption data recorded at a sampling rate of 1024 Hz for exactly 1 second (1024 samples). The columns are `time` (in seconds) and `power` (in watts).
2. `/home/user/latency_logs.csv`: Contains execution latencies of 5000 requests. The columns are `request_id` and `latency_ms`.

**Your Tasks:**

1. **Spectroscopy / Signal Processing:**
   Analyze `/home/user/cpu_signal.csv` using a Fast Fourier Transform (FFT). Identify the top two strictly positive, non-DC (frequency > 0) dominant frequencies in the power signal. Sort them in descending order of their magnitudes. 

2. **Density Estimation:**
   Analyze `/home/user/latency_logs.csv`. 
   - Calculate the 99th percentile of the `latency_ms` data.
   - Fit a Gaussian Kernel Density Estimate (KDE) to the `latency_ms` data using Scott's Rule for the bandwidth (this is the default in `scipy.stats.gaussian_kde`).
   - Evaluate this KDE on a linear grid from 0 to 200 with exactly 2000 points (`numpy.linspace(0, 200, 2000)`). Identify the `latency_ms` value on this grid where the KDE reaches its absolute maximum (the peak/mode).

3. **Convergence Testing:**
   We want to know how many latency samples are needed to confidently estimate the mean latency. Calculate the cumulative Standard Error of the Mean (SEM) for the `latency_ms` data as you add samples one by one (starting from the 2nd sample). 
   - SEM for $N$ samples is defined as the sample standard deviation (with 1 degree of freedom, `ddof=1`) divided by $\sqrt{N}$.
   - Find the minimum number of samples $N$ (where $N \ge 2$) such that the cumulative SEM strictly falls below `0.20`.

**Output Specification:**
Create a JSON file at `/home/user/profiling_report.json` with the following schema containing your computed results. Round floating-point numbers to two decimal places.

```json
{
  "dominant_frequencies": [ <highest_magnitude_freq>, <second_highest_magnitude_freq> ],
  "latency_kde_peak": <latency_at_kde_peak>,
  "latency_p99": <99th_percentile_latency>,
  "convergence_n": <integer_N>
}
```
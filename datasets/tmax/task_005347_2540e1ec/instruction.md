You are a performance engineer profiling a numerical integrator. Recently, the integrator has been diverging on certain workloads due to a suspected step-size adaptation resonance. 

I have extracted the error metrics over a 10-second simulation window (sampled at 100 Hz, giving 1000 samples) into a CSV file located at `/home/user/sim_data.csv`. The CSV has three columns: `time`, `stable_err`, and `unstable_err`.

Your task is to write a Go program at `/home/user/analyze.go` that processes this CSV and extracts the following analytical metrics:
1. **Dominant Frequency**: Perform a Fourier Transform (FFT or DFT) on the `unstable_err` signal. Find the frequency (in Hz) with the highest magnitude (ignoring the DC component / 0 Hz).
2. **Distribution Distance**: Calculate the 1st Wasserstein distance between the empirical distributions of `stable_err` and `unstable_err`. For two equal-sized 1D empirical samples, this is calculated as the mean of the absolute differences between the sorted samples: `mean(|sort(stable_err) - sort(unstable_err)|)`.
3. **Bootstrap Confidence Interval**: Compute the 95% bootstrap confidence interval for the *mean* of `unstable_err`. 
   - Use exactly `1000` bootstrap iterations.
   - For each iteration, sample with replacement from `unstable_err` to create a sample of the same size (1000), and compute its mean.
   - Use `math/rand.New(math/rand.NewSource(42))` created exactly once before the loop to drive the sampling (use `rand.Intn(1000)` to pick indices).
   - After generating the 1000 bootstrap means, sort them and select the 2.5th percentile (index 25) and 97.5th percentile (index 975) as the lower and upper bounds, respectively.

Your Go program must write the results to `/home/user/report.json` with the following format (round all float values to 2 decimal places):
```json
{
  "dominant_frequency": 8.00,
  "wasserstein_distance": 1.23,
  "bootstrap_ci_lower": -0.05,
  "bootstrap_ci_upper": 0.05
}
```

You may use standard Go libraries or initialize a Go module and use `gonum.org/v1/gonum` for the math/FFT operations. Run your program and ensure the JSON file is generated correctly.
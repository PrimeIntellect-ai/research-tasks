You are a performance engineer tasked with profiling a new microservice architecture to ensure a recent code change hasn't introduced tail-latency regressions. 

You have been provided with two files in your home directory (`/home/user`):
1. `/home/user/reference_data.txt`: A reference dataset of historical request latencies (in milliseconds), containing one floating-point number per line.
2. `/home/user/model.go`: A Go file (part of the `main` package) containing a latency generator function for the new architecture: `func LatencySample(rng *rand.Rand) float64`.

Your task is to write a Go program (save it as `/home/user/simulate.go`, in package `main`) that performs a Monte Carlo simulation to estimate the new latency distribution and compares it against the historical reference dataset. 

Specifically, your program must:
1. Parse `/home/user/reference_data.txt` and calculate the 95th percentile (P95) latency of the historical data. 
2. Perform a Monte Carlo simulation by drawing exactly 100,000 samples from `LatencySample()`. You MUST initialize the random number generator with a seed of `42` like so: `rng := rand.New(rand.NewSource(42))`.
3. Calculate the 95th percentile (P95) of the simulated samples. 
   *(Note: For calculating the 95th percentile in both datasets, use the nearest-rank method: sort the data in ascending order and pick the value at index `ceil(0.95 * N) - 1`, where N is the number of items).*
4. Perform a regression test: if the simulated P95 is strictly greater than `1.20 * historical_P95`, it is considered a regression.
5. Output the results to a log file located at `/home/user/regression_report.txt`.

The format of `/home/user/regression_report.txt` must be exactly as follows (round the latency values to exactly two decimal places using `fmt.Sprintf("%.2f", val)`):
```
Historical P95: <value>
Simulated P95: <value>
Status: <REGRESSION DETECTED | PERFORMANCE OK>
```

You can execute your code using `go run model.go simulate.go`. Do not modify `model.go`.
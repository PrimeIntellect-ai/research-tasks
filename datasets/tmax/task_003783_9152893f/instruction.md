You are a Site Reliability Engineer (SRE) investigating an issue with your team's custom Go-based SLA monitoring service. The service aggregates uptime metrics from thousands of containers, but recently it has been crashing and reporting mathematically incorrect average uptimes, triggering false alerts.

The source code is located in `/home/user/uptime-app/`. 

Your objectives are to fix the bugs, ensure stability, and generate the correct final report:

1. **Format Parsing Edge-Case Repair**: Look at `calc.go`. The function `ParseMetric(val string)` is crashing or returning errors on some of the messy raw container logs. Inspect the logs provided in `/home/user/uptime-app/logs/raw_metrics.txt` to understand the anomalies (e.g., trailing whitespace, detached '%' signs, carriage returns). Fix `ParseMetric` to correctly extract the numerical values and ignore any surrounding whitespace or `%` characters. 

2. **Fuzz Testing**: To prevent future parsing crashes, write a standard Go fuzz test in `/home/user/uptime-app/calc_test.go` for the `ParseMetric` function. The fuzzer should ensure that `ParseMetric` never panics, regardless of the string input, and correctly parses valid variations.

3. **Precision Loss Tracking**: The function `CalculateAverage(metrics []float32) float32` suffers from severe precision loss. The fleet produces over 100,000 log entries per day. Summing that many `float32` values causes absorptive errors (the accumulator grows too large to accurately add small floating-point values), resulting in a mathematically incorrect SLA average. Rewrite the calculation logic to use `float64` internally for accumulation to prevent precision loss, and return the precise `float64` average. Change the signature to `CalculateAverage(metrics []float32) float64`.

4. **Generate Final Report**: Write a `main.go` file in `/home/user/uptime-app/` that reads `/home/user/uptime-app/logs/raw_metrics.txt`, parses every line using your fixed `ParseMetric` function, collects them in a slice, and calculates the true average using your updated `CalculateAverage`. 

Save the final calculated average to `/home/user/result.txt`, formatted to exactly 5 decimal places (e.g., `99.99450`).

Do not use any external dependencies outside the Go standard library.
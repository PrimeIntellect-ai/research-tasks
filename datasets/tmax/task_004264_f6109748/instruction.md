You are a data scientist troubleshooting numerical stability issues in a data processing pipeline. You have a dataset of high-precision sensor readings located at `/home/user/sensor_data.txt`. The readings are very large baseline numbers with very small fluctuations.

When fitting models with these values, the legacy system calculates the variance naively, resulting in catastrophic cancellation and loss of significance (returning 0 or incorrect values).

Your task is to write a Go program at `/home/user/compute_variance.go` that:
1. Reads the float values from `/home/user/sensor_data.txt` (one per line).
2. Calculates the **sample variance** (using $n-1$ degrees of freedom) of these numbers using a numerically stable algorithm (such as Welford's algorithm or a two-pass mean-centered approach) using `float64`.
3. Prints the resulting sample variance formatted to exactly 8 decimal places.

After writing the program, compile and run it, and direct its output to `/home/user/result.txt`. 

Make sure your final output file `/home/user/result.txt` contains only the formatted numeric value.
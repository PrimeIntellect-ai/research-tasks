You are a DevOps engineer debugging a failed log processing job. We have a C program at `/home/user/sensor_stats.c` that reads a list of floating-point sensor readings from `/home/user/data.txt` and calculates their mean, variance, and standard deviation.

Currently, the pipeline is failing for two reasons:
1. **Build Failure:** The program fails to compile. You need to diagnose the missing flags or syntax issues and successfully compile it to `/home/user/sensor_stats`.
2. **Numerical Instability / Precision Loss:** Once you get it to build and run it, you'll notice the output in `/home/user/output.log` reports a variance and standard deviation of `0.000000` (or sometimes `NaN`). This is due to catastrophic cancellation and precision loss, as the sensor readings are large but have very small variations. 

Your task:
1. Fix the build error (compile the executable to `/home/user/sensor_stats`).
2. Modify `/home/user/sensor_stats.c` to fix the precision loss and numerical instability. You must upgrade the relevant data types and math functions to double precision (`double`) to correctly compute the variance and standard deviation.
3. Run the compiled executable so that the correct results are written to `/home/user/output.log`.

The output format in `/home/user/output.log` must remain exactly:
```
Mean: [value]
Variance: [value]
StdDev: [value]
```
where `[value]` is formatted to 6 decimal places (e.g., `%.6f` or `%.6lf`).

Do not change the underlying statistical formulas (population variance is expected: `E[X^2] - (E[X])^2`); simply fix the precision loss problem so the math evaluates correctly.
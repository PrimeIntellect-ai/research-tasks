You are a data engineer building an ETL pipeline to process streaming sensor data. Our data is currently locked inside a video file, and the pipeline suffers from missing frames (an issue analogous to silent NaN introduction when integers are coerced to floats).

Your task is to build a C-based pipeline that extracts the data, handles the missing values, and applies an online Bayesian filter to estimate the underlying signal mean.

Step 1: Write the C Bayesian Filter
Write a C program that reads a continuous stream of binary `double` values (64-bit IEEE 754, little-endian) from `stdin` until EOF.
The program must implement an online Bayesian estimator for the mean of a normal distribution with the following specifications:
- Initial prior mean $\mu_0 = 0.0$
- Initial prior variance $\sigma^2_0 = 100.0$
- Known observation variance $\sigma^2_{obs} = 10.0$

For each incoming observation $x$:
- If $x$ is exactly `-999.0`, it is considered a missing value (dropped frame). Do NOT update the posterior mean or variance. Instead, output the *current* posterior mean.
- If $x \neq -999.0$, update the posterior mean and variance using the standard Bayesian conjugate update for a normal mean with known observation variance. Output the *new* posterior mean.
- The output must be written to `stdout` as binary `double` values.

Compile your program to exactly `/home/user/bayesian_filter` (it must be executable).

Step 2: Video ETL Processing
We have a video feed at `/app/stream.mp4`. Each frame represents a single sensor reading.
- Extract the average grayscale brightness (from 0.0 to 255.0) of each frame in the video in chronological order.
- If a frame's average brightness is strictly less than `10.0`, it represents a dropped signal. Record this as `-999.0`.
- Otherwise, record the exact average brightness.
- Save this sequence of raw extracted `double` values as a binary file to `/home/user/raw_measurements.bin`.

Step 3: Integration
Pipe `/home/user/raw_measurements.bin` through your `/home/user/bayesian_filter` program and save the resulting binary `double` stream to `/home/user/smoothed_measurements.bin`.
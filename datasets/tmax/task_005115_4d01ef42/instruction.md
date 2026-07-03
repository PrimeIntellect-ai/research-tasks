You are an ETL data engineer building a lightweight inference pipeline for a predictive maintenance system. You need to join sensor data from two different sources and implement a high-performance C program to perform model inference and benchmarking.

We have two CSV files in `/home/user/`:
1. `/home/user/sensor_temp.csv` (columns: `id,temperature`)
2. `/home/user/sensor_vib.csv` (columns: `id,vibration`)

Both files are sorted by `id`.

Your task consists of three parts:

**Part 1: Multi-source Data Joining**
Write a bash script at `/home/user/join_data.sh` that joins the two CSV files by the `id` column. The output should be saved to `/home/user/joined_sensor_data.csv` with the header `id,temperature,vibration`. Ensure the header only appears once.

**Part 2: Probabilistic Inference and Linear Algebra in C**
Write a C program at `/home/user/infer.c` that reads `/home/user/joined_sensor_data.csv`. 
We have a pre-trained probabilistic logistic regression model. The probability of a machine failure (Class 1) given temperature ($t$) and vibration ($v$) is modeled as:
$P(y=1 | x) = \sigma(W \cdot x + b)$
Where:
- $\sigma(z) = \frac{1}{1 + e^{-z}}$
- The weight vector $W = [0.5, 1.2]$ (for temperature and vibration, respectively).
- The bias $b = -15.0$.

For each row (excluding the header), your C program must:
1. Parse the `id` (int), `temperature` (float), and `vibration` (float).
2. Calculate the probability $p$ of failure using the formula above.
3. Determine the predicted class (1 if $p > 0.5$, else 0).
4. Write the results to `/home/user/predictions.csv` with the header `id,probability,class`. Format the probability to exactly 4 decimal places (`%.4f`).

**Part 3: Inference Performance Benchmarking**
In your C program, use `clock_gettime(CLOCK_MONOTONIC, ...)` to measure *only* the total time taken for the mathematical inference loop (i.e., start the timer after reading the file into memory or before the loop, and stop it immediately after calculating the probabilities, excluding file I/O where possible). 
Output the elapsed time in microseconds to `/home/user/benchmark.txt` in exactly this format:
`Inference Time: <time_in_microseconds> us`

Compile your C program into an executable named `/home/user/infer_model` and link the math library (`-lm`). Execute the bash script and then the C program to generate the required outputs.
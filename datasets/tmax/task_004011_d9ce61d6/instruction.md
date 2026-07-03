You are an AI assistant helping a data scientist researcher organize a massive repository of sensor telemetry. 

The researcher previously tried to filter out "noisy" sensor datasets using a Python script, but they accidentally introduced data leakage by scaling the features using global statistics computed across the entire dataset before splitting. This caused normal datasets to be flagged as anomalous.

We need to implement a strict, per-file anomaly detector written purely in C to ensure numerical accuracy, fast execution, and strict isolation between datasets to prevent leakage.

Here is your task:

1. **Extract Hyperparameters**: There is an image located at `/app/config.png` containing the mathematical parameters for our anomaly detection algorithm. You must extract these parameters (Target Column, Bootstrap Iterations, and Threshold).
2. **Implement the Detector in C**: Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`. 
   The program must accept exactly one argument: the path to a CSV file.
   Usage: `./detector <path_to_csv>`
3. **Algorithm Specifications**:
   - Parse the CSV file (it has no headers, 3 comma-separated floating-point columns).
   - Extract the `TARGET_COL` specified in the image (1-indexed).
   - **Feature Engineering**: Compute the absolute differences between consecutive rows for that column: $d_i = |x_i - x_{i-1}|$. If there are $N$ rows, there will be $N-1$ differences.
   - **Sampling and Bootstrapping**: Perform a numerical bootstrap on these differences to estimate the volatility. Sample the differences *with replacement* $N-1$ times, and calculate the mean of the resampled differences. Repeat this process `BOOTSTRAP_B` times (from the image). Use a fixed random seed (e.g., `srand(42)`) for reproducibility.
   - **Bayesian/Statistical Threshold**: Find the 2.5th percentile of your bootstrap means (the lower bound of the 95% confidence interval). Sort the bootstrap means to find this value.
   - If this lower bound is **strictly greater** than the `THRESHOLD` from the image, print exactly `REJECT` to standard output. Otherwise, print `ACCEPT`.
   - The program must terminate with exit code 0.
4. **Validation**: We have an adversarial evaluation corpus.
   - `/app/corpora/clean/`: Contains valid sensor readings. Your detector MUST `ACCEPT` 100% of these.
   - `/app/corpora/evil/`: Contains anomalous files simulating sensor drift. Your detector MUST `REJECT` 100% of these.

Ensure your C code relies only on standard libraries (`stdio.h`, `stdlib.h`, `math.h`, `string.h`). You may use `tesseract` to read the image. Compile your code with `gcc -O3 -lm`. 

Your final executable must be at `/home/user/detector`.
You are a data engineer building a reproducible ETL pipeline to process noisy sensor data. The core data processing must be implemented in C for performance, and you need to build the pipeline to ensure computational reproducibility and statistical rigor. 

Your task is to write a C program, compile it, and write a Bash script to verify the reproducibility of your pipeline.

**Step 1: The C ETL Processor**
Write a C program at `/home/user/etl_processor.c` that does the following:
1. Takes exactly three command-line arguments: `<input_file> <seed> <num_bootstraps>`
2. Reads the `<input_file>` which contains one floating-point number per line. Let $N$ be the number of values.
3. Initializes the random number generator using `srand(seed)`.
4. Performs Bootstrap Sampling:
   - For `num_bootstraps` iterations, sample exactly $N$ values from the dataset *with replacement* using `rand() % N` to select indices.
   - Calculate the sample mean ($\bar{x}_b$) for each bootstrap sample $b$.
   - Calculate the overall average of the bootstrap means ($\mu_{boot}$) and the standard deviation of the bootstrap means (the bootstrap standard error, $SE_{boot}$).
5. Performs a Bayesian Update:
   - Assume the sensor readings are drawn from a Normal distribution with a known variance $\sigma^2 = 1.0$.
   - Assume a prior distribution for the true mean $\mu$ as Normal with prior mean $\mu_0 = 0.0$ and prior variance $\sigma_0^2 = 100.0$.
   - Use the overall bootstrap mean $\mu_{boot}$ as your observed sample mean to compute the posterior mean of $\mu$. 
   - The formula for the posterior mean is: 
     $$\mu_{post} = \frac{\frac{\mu_0}{\sigma_0^2} + \frac{N \cdot \mu_{boot}}{\sigma^2}}{\frac{1}{\sigma_0^2} + \frac{N}{\sigma^2}}$$
6. Writes the results to `/home/user/etl_output.csv` in the exact format:
   `seed,posterior_mean,bootstrap_se`
   (Format floats to 6 decimal places, e.g., `%.6f`).

**Step 2: Compilation**
Compile your program to `/home/user/etl_processor` using `gcc` with standard mathematical libraries (`-lm`).

**Step 3: Reproducibility Testing Pipeline**
Write a bash script at `/home/user/pipeline_test.sh` that:
1. Runs the compiled `etl_processor` twice, both times using `/home/user/sensor_data.csv` as input, `42` as the seed, and `1000` as the number of bootstraps.
2. Saves the output of the first run to `/home/user/run1.csv` and the second run to `/home/user/run2.csv`.
3. Compares the two files. If they are exactly identical, write `REPRODUCIBLE: YES` to `/home/user/test_result.txt`. Otherwise, write `REPRODUCIBLE: NO`.

**Notes:**
- The dataset `/home/user/sensor_data.csv` has already been created for you.
- Ensure your C code correctly parses the floating point data and handles up to 1000 lines.
- Do not use any external C libraries beyond the standard library (`stdio.h`, `stdlib.h`, `math.h`).
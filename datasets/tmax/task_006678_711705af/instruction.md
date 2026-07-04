You are an ML engineer preparing a robust data processing pipeline. Before feeding sensor data into our neural network, we need to estimate the reliability of the baseline trend using bootstrap resampling.

We have a dataset at `/home/user/sensor_data.csv` with two columns: `x` and `y` (including a header row). There are exactly 100 data points.

Your task is to write a C program named `/home/user/bootstrap.c` that does the following:
1. Reads the `x` and `y` values from the CSV.
2. Performs a Simple Linear Regression (least squares fit) to find the slope ($m$) of the line $y = mx + c$.
3. Uses bootstrap resampling to estimate the 95% confidence interval for the slope.
    - Perform exactly `10000` bootstrap iterations.
    - In each iteration, sample 100 pairs from the original data *with replacement*, compute the slope, and store it.
    - Sort the 10,000 computed slopes.
    - The 95% confidence interval bounds are the 2.5th percentile and 97.5th percentile values (which correspond to the sorted array indices 249 and 9749, assuming 0-based indexing).
4. To ensure perfectly reproducible results across any standard library version, you **must** use the following custom pseudo-random number generator to select indices:
   ```c
   unsigned long int state = 42;
   int get_random_index(int num_points) {
       state = (1103515245 * state + 12345) % 2147483648;
       return state % num_points;
   }
   ```
   *Note: Call `get_random_index(100)` exactly 100 times per iteration to build each bootstrap sample, sequentially from the 1st iteration to the 10,000th.*

5. The program should output a single line to a file named `/home/user/ci_output.txt` strictly in this format:
   `Slope CI: [lower_bound, upper_bound]`
   Format the floats to exactly 4 decimal places.

Compile the program using `gcc`, run it, and ensure `/home/user/ci_output.txt` is created with the correct confidence interval.
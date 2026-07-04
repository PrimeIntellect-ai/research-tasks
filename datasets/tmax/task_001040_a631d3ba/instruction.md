You are a data analyst working on a C-based data processing pipeline. We have a set of experimental CSV data files in `/home/user/data/` that contain sensor readings. 

The files have two columns: `id` and `value`. 
Unfortunately, the data is noisy. There are missing values (empty strings in the `value` column, e.g., `2,`), which naive C parsers like `atoi` might silently convert to `0`, ruining the analysis. There are also extreme outliers caused by sensor glitches.

Your task is to implement a robust pipeline in C and Bash to process these files, explicitly handling missing values and tracking outliers using a Bayesian conjugate prior update.

**Step 1: Write `/home/user/process_data.c`**
Write a C program that takes a single file path as a command-line argument.
The program must read the CSV file line by line and perform a sequential Bayesian update for the mean of the data, assuming a Normal-Normal conjugate prior.

*   **Initialization:**
    *   Prior Mean ($\mu_0$): `0.0`
    *   Prior Variance ($\sigma_0^2$): `100.0`
    *   Known Likelihood Variance for each observation ($\sigma^2$): `10.0`
*   **Processing Rules for each line:**
    1.  Parse the `id` and `value`. Both are expected to be integers, but `value` can be missing.
    2.  If `value` is missing (i.e., nothing after the comma), increment a `missing_count` and skip the Bayesian update for this line.
    3.  If `value` is present, check if it's an outlier. An observation $x$ is an outlier if its distance from the current posterior mean is greater than 3 standard deviations of the predictive distribution: 
        $|x - \mu_n| > 3 \sqrt{\sigma_n^2 + \sigma^2}$
    4.  If it is an outlier, increment an `outlier_count` and skip the Bayesian update.
    5.  If it is valid (not missing, not an outlier), increment a `valid_count` and update the posterior mean and variance using the standard conjugate prior formulas:
        *   $\mu_{n+1} = \frac{\sigma^2 \mu_n + \sigma_n^2 x}{\sigma_n^2 + \sigma^2}$
        *   $\sigma_{n+1}^2 = \frac{\sigma_n^2 \sigma^2}{\sigma_n^2 + \sigma^2}$
*   **Output:**
    The C program must print exactly one line to standard output in this exact format (floating point numbers should be printed with exactly 2 decimal places using `%.2f`):
    `Valid: <v_count>, Missing: <m_count>, Outliers: <o_count>, Final Mean: <mean>`

**Step 2: Write `/home/user/run_experiments.sh`**
Write a Bash script that automates the experiment tracking:
1. Compiles `/home/user/process_data.c` into an executable named `process_data` (use `gcc -O2 -lm`).
2. Iterates over all `.csv` files in `/home/user/data/` in alphabetical order.
3. Runs the compiled executable on each file.
4. Appends the results to a log file at `/home/user/results.log`.

Each line in `/home/user/results.log` must be formatted exactly as follows:
`File: <filename> | <c_program_output>`
*(Example: `File: exp1.csv | Valid: 3, Missing: 1, Outliers: 1, Final Mean: 4.84`)*

Complete the task by ensuring both the C source file and Bash script are created and that you have executed `/home/user/run_experiments.sh` so that `/home/user/results.log` is generated.
You are assisting a data researcher who is organizing a large repository of datasets. Recently, a silent bug in a pandas pipeline corrupted several datasets by interpolating missing values, converting what should be pure integer columns into floating-point numbers with fractional parts. 

Your objective is to write a robust C++ classifier that detects whether a dataset is "clean" (pure) or "evil" (corrupted), using statistical techniques.

Here is the precise workflow you must implement:

1. **Extract Parameters:**
   There is a scanned configuration image located at `/app/config.png`. You must extract the text from this image (e.g., using `tesseract`) to find three critical parameters:
   - `BOOTSTRAP_ITERS`
   - `PRIOR_ALPHA`
   - `PRIOR_BETA`
   - `POSTERIOR_THRESHOLD`

2. **Implement the C++ Classifier:**
   Write a C++ program at `/home/user/classifier.cpp` and compile it to `/home/user/classifier`.
   The program must accept a single command-line argument: the path to a CSV file.
   It must output exactly `CLEAN` or `EVIL` to standard output (with a newline).

   **The Algorithm:**
   * **Parse the CSV:** The CSV has no header. Read it into a 2D array of `double`.
   * **Dimensionality Reduction:** Find the single column with the highest variance. Discard all other columns. You will only analyze this highest-variance column.
   * **Sampling and Bootstrap:** Perform `BOOTSTRAP_ITERS` bootstrap resamples (with replacement) of this chosen column. Each resample should be the same size $N$ as the original column.
   * **Bayesian Inference:** For each bootstrap sample, count $k$, the number of "non-integer" values (defined as having a fractional part greater than `1e-5` or less than `-1e-5`). 
     Calculate the posterior expected value of the corruption rate using a Beta-Binomial conjugate update:
     $E[\theta] = \frac{k + \text{PRIOR\_ALPHA}}{N + \text{PRIOR\_ALPHA} + \text{PRIOR\_BETA}}$
   * **Decision:** Calculate the average $E[\theta]$ across all bootstrap samples. If this average is strictly greater than `POSTERIOR_THRESHOLD`, the program must print `EVIL`. Otherwise, print `CLEAN`.

3. **Validation:**
   There are two directories containing test CSVs:
   - `/app/corpus/clean/`
   - `/app/corpus/evil/`
   Your compiled `/home/user/classifier` must correctly identify 100% of the files in both directories.

Use standard C++ libraries. You may use shell commands to explore the environment and compile your code.
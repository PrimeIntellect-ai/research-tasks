You are an AI assistant helping a data researcher organize and analyze a series of experimental datasets. 

The researcher uses a specific Python package for exact statistical tests, but the provided source code for it is currently broken and failing to compile. Furthermore, they need a robust processing script that can take their raw dataset files, apply exact statistical tests, perform dimensionality reduction, and extract confidence intervals, all while ensuring strict numerical formatting.

Your tasks are:

1. **Fix and Install the Vendored Package:**
   There is a vendored package located at `/app/fisher-0.1.9`. This is a real third-party package (`fisher`) used to calculate Fisher's exact test. However, the researcher accidentally corrupted the package's compilation configuration when trying to optimize it. 
   Find the issue preventing the package from compiling, fix it, and install the package into the current Python environment (e.g., using `pip install -e .`).

2. **Create the Data Processing Script:**
   Write a Python script at `/home/user/process_dataset.py`. This script will be called with a single command-line argument: the path to a CSV file.

   The CSV file will always have exactly five columns with a header row: `cat1,cat2,val1,val2,val3`.
   - `cat1` and `cat2` contain binary integer values (`0` or `1`).
   - `val1`, `val2`, and `val3` contain floating-point numbers.

   Your script must perform the following pipeline:
   
   **A. Hypothesis Testing (Fisher's Exact Test):**
   - Construct a 2x2 contingency table from `cat1` and `cat2`. The table counts should represent:
     `[[count(0,0), count(0,1)], [count(1,0), count(1,1)]]`
   - Use the installed `fisher` module (`fisher.pvalue`) to compute the two-tailed p-value for this contingency table.

   **B. Dimensionality Reduction (PCA via SVD):**
   - Extract the matrix of continuous variables (`val1`, `val2`, `val3`).
   - Mean-center the continuous data (subtract the mean of each column from the column).
   - Perform Singular Value Decomposition (SVD) on the centered data to extract the *first principal component* (the right singular vector corresponding to the largest singular value).
   - **Numerical convention:** To resolve the sign ambiguity of SVD, if the first element of this principal component vector is negative, multiply the entire vector by `-1`.

   **C. Confidence Intervals:**
   - Compute the 95% confidence interval for the mean of the `val1` column using the standard Student's t-distribution approach. Use the sample standard deviation (with 1 degree of freedom for the variance denominator). 

   **D. Output:**
   Your script must print exactly one line to standard output containing a valid JSON object with the following keys, with all floating-point numbers rounded to exactly 4 decimal places:
   - `"fisher_p"`: The two-tailed p-value (float).
   - `"pc1"`: The first principal component vector as a list of 3 floats.
   - `"val1_ci"`: A list of 2 floats representing the 95% confidence interval `[lower_bound, upper_bound]`.

   *Example Output:*
   `{"fisher_p": 0.4512, "pc1": [0.5123, 0.4001, 0.7599], "val1_ci": [-2.3451, 5.6789]}`

Ensure your script is perfectly deterministic and handles numerical operations cleanly, as it will be rigorously tested against an exact reference implementation.
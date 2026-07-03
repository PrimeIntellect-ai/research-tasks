You are a data scientist dealing with a problematic dataset. Your high-level tools (like Pandas) keep silently corrupting integer IDs into floats because of missing values (NaN introduction). To solve this, you need to write a low-level, strict data processing pipeline in C.

Write a C program that performs data cleaning, aggregation, and bootstrap-based confidence interval estimation.

**Requirements:**
1. **Input Data**: A CSV file located at `/home/user/measurements.csv`. The file has three columns: `machine_id` (integer), `measurement` (float), and `flag` (string). There is a header row.
2. **Data Cleaning**:
   - Parse the CSV.
   - Discard any row where the `machine_id` is empty (missing).
   - Discard any row where the `flag` is NOT exactly the string `"VALID"`.
3. **Aggregation**:
   - Calculate the mean of the `measurement` values for `machine_id` 1.
   - Calculate the mean of the `measurement` values for `machine_id` 2.
4. **Bootstrapping (Confidence Interval)**:
   - Extract all valid `measurement` values for `machine_id` 1. Let the count of these values be N.
   - Perform a bootstrap analysis to find the 95% confidence interval of the mean for `machine_id` 1.
   - Generate 10,000 bootstrap samples. For each sample, draw N values with replacement from the valid measurements of `machine_id` 1, and calculate the mean.
   - Sort these 10,000 means to find the 2.5th percentile (index 250, 0-indexed) and the 97.5th percentile (index 9750, 0-indexed).
   - **Crucial**: To ensure reproducibility, you must initialize the random number generator strictly by calling `srand(42)` exactly once before your bootstrapping loop. Use `rand() % N` to select indices for the bootstrap sample.
5. **Output**:
   - Write the results to a file named `/home/user/report.txt`.
   - The file must contain exactly these four lines (format floats to 4 decimal places):
     ```
     Mean 1: <value>
     Mean 2: <value>
     CI 1 Lower: <value>
     CI 1 Upper: <value>
     ```

**Execution**:
Compile your C code to an executable at `/home/user/analyze` and run it so that `/home/user/report.txt` is generated. 

Note: You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`).
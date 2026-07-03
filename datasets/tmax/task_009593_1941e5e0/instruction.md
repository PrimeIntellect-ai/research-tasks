You are acting as a Data Engineer building a high-performance ETL pipeline component in C.

You need to process data from two sensor streams, join them, enforce strict schema validation, compute the sample covariance matrix of the features, and calculate empirical probabilities for a Naive Bayes classifier. 

Write a C program that performs the following steps:

1. **Multi-source Data Joining & Schema Enforcement:**
   Read two CSV files located at `/home/user/sensors.csv` and `/home/user/labels.csv`.
   - `sensors.csv` format: `id,sensor1,sensor2,sensor3`
   - `labels.csv` format: `id,label`
   
   You must perform an inner join on the `id` column.
   **Schema Rules:** Reject and drop any joined row if:
   - Any of `sensor1`, `sensor2`, or `sensor3` cannot be successfully parsed as a floating-point number.
   - `label` is missing or is NOT exactly `0` or `1` (integer).
   - A row exists in one file but has no matching `id` in the other.

2. **Correlation and Covariance Analysis:**
   For the cleaned, joined dataset, compute the 3x3 sample covariance matrix for `[sensor1, sensor2, sensor3]`. Use the standard unbiased sample covariance formula (dividing by N-1).

3. **Bayesian Inference Summaries:**
   Compute the following empirical probabilities based on the cleaned dataset:
   - The prior probability of class 1: `P(label = 1)`
   - The conditional probability of sensor1 being greater than 0.5 given label 1: `P(sensor1 > 0.5 | label = 1)`
   - The conditional probability of sensor1 being greater than 0.5 given label 0: `P(sensor1 > 0.5 | label = 0)`

4. **Output Generation:**
   The C program must output the exact results to a JSON file at `/home/user/etl_results.json`. 
   The JSON file must have exactly this structure and key naming (format the floats to 4 decimal places):
   ```json
   {
     "valid_rows": <integer>,
     "covariance_matrix": [
       [<float>, <float>, <float>],
       [<float>, <float>, <float>],
       [<float>, <float>, <float>]
     ],
     "p_label_1": <float>,
     "p_s1_gt_half_given_label_1": <float>,
     "p_s1_gt_half_given_label_0": <float>
   }
   ```
   *Note: The covariance matrix array corresponds to rows and columns for sensor1, sensor2, sensor3 in that order.*

**Requirements:**
- You MUST write the solution in C. You can create your source file(s) in `/home/user/` and compile them using `gcc`.
- Do not use any external dependencies or libraries outside of the C standard library (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, etc.).
- Ensure your output JSON is valid and the floats are rounded to 4 decimal places (e.g., using `"%.4f"`).
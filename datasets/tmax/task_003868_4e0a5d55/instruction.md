You are a data engineer building a high-performance ETL and feature extraction pipeline in C. You need to process a dataset containing sensor readings and text annotations, handle missing values, remove outliers, engineer new features from the text, and split the data for cross-validation.

Write a C program that performs this ETL pipeline. 

**Input:**
A CSV file located at `/home/user/raw_data.csv` with the header `id,sensor_val,text_note`.
- `id`: integer
- `sensor_val`: double (may be empty, i.e., consecutive commas `,,`)
- `text_note`: string (may be empty, may contain spaces)

**Pipeline Requirements:**
1. **Missing Value Handling**: First, calculate the mean of all present `sensor_val` entries. Impute any missing `sensor_val` entries with this mean.
2. **Outlier Removal**: Calculate the population standard deviation (using N, not N-1) of the *imputed* `sensor_val` dataset. Remove any rows where the absolute difference between the imputed `sensor_val` and the mean is strictly greater than `2.0 * standard_deviation`.
3. **Feature Engineering (Tokenization)**: For the `text_note` field, count the number of space-separated words (tokens). Multiple consecutive spaces should not be counted as extra words. An empty text note has 0 tokens.
4. **Cross-Validation Prep**: Assign each surviving row to a fold by taking `id % 3` (resulting in fold 0, 1, or 2).

**Outputs:**
1. The program must compile successfully. Name your source `pipeline.c` and compile it to `/home/user/pipeline` (e.g., `gcc -O3 -o /home/user/pipeline pipeline.c -lm`).
2. Run your compiled program, reading `/home/user/raw_data.csv` and writing the processed data to `/home/user/clean_features.csv`.
   - The output CSV must have the header: `id,imputed_sensor_val,token_count,fold`
   - Print `imputed_sensor_val` to 4 decimal places (e.g., `%.4f`).
3. Your program must also write an experiment tracking log to `/home/user/experiment_log.txt` with exactly the following four lines (replace bracketed items with your calculated values to 4 decimal places where applicable):
   ```
   Original Rows: [count]
   Mean: [mean]
   StdDev: [std_dev]
   Surviving Rows: [count]
   ```
   *Note: "Original Rows" does not include the header.*

Assume the CSV has at most 1000 rows and lines are at most 512 characters long. All text notes consist only of alphanumeric characters and spaces.
You are an AI assistant helping a researcher organize and analyze a collection of datasets. The researcher has extracted summary statistics for several datasets and saved them in a CSV file, but the data is messy and needs to be analyzed programmatically.

The metadata file is located at `/home/user/datasets_meta.csv` and contains the following columns: `dataset_id`, `num_rows`, `num_features`, `missing_pct`, `feature_mean`, `feature_std`.

Perform the following steps using Python:

**1. Data Cleaning & Schema Enforcement**
Filter the dataset to enforce validity constraints:
- `num_rows` must be strictly greater than 0.
- `feature_std` must be strictly greater than 0.
Drop any rows that violate these constraints.

**2. Missing Value Handling**
Some datasets have missing values (empty strings/nulls) in the `missing_pct` column. Fill these missing values with the **median** of the valid `missing_pct` values from the cleaned dataset from Step 1.

**3. Similarity Search**
The researcher wants to find datasets similar to the target dataset, which has the `dataset_id` of `DS_Target`.
- Standardize the 5 numerical columns (`num_rows`, `num_features`, `missing_pct`, `feature_mean`, `feature_std`) by subtracting the mean and dividing by the sample standard deviation (ddof=1) of the cleaned dataset.
- Calculate the Euclidean distance between `DS_Target` and all other datasets using these standardized features.
- Identify the 2 closest datasets to `DS_Target` (excluding `DS_Target` itself).

**4. Hypothesis Testing**
The researcher wants to know if the underlying data distribution of `DS_Target` is statistically different from its *single closest* matching dataset found in Step 3.
- Treat `feature_mean` as the sample mean, `feature_std` as the sample standard deviation, and `num_rows` as the sample size (N).
- Perform a two-tailed Welch's t-test (independent samples t-test with unequal variances) between `DS_Target` and its closest dataset.

**Output Specification**
Create a JSON file at `/home/user/report.json` with exactly the following structure and keys:
```json
{
  "cleaned_dataset_count": <integer, total number of datasets after Step 1>,
  "closest_datasets": [<string: id_of_closest>, <string: id_of_second_closest>],
  "t_stat": <float, rounded to 2 decimal places>,
  "p_value": <float, rounded to 4 decimal places>,
  "is_significantly_different": <boolean, true if p-value < 0.05, false otherwise>
}
```

Do not use hardcoded values; your Python script should compute the results dynamically.
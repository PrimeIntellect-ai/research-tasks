You are an ML Engineer preparing a training dataset for a used car pricing model. The raw dataset is imbalanced and lacks important derived features.

Your raw data is located at `/home/user/raw_cars.csv`. It contains the following columns: `make`, `year`, `mileage`, and `price`. 

Your task is to write a Python script (and install any necessary libraries like `pandas` using pip) that does the following:

1. **Feature Engineering**:
   - Create a new column called `vehicle_age` calculated as: `2024 - year + 1`.
   - Create a new column called `mileage_per_year` calculated as: `mileage / vehicle_age`.
   - Drop the `year` and `mileage` columns. Keep only `make`, `vehicle_age`, `mileage_per_year`, and `price`.

2. **Bootstrapping (Oversampling)**:
   - The dataset contains two classes in the `make` column: "Standard" and "Luxury".
   - There are significantly fewer "Luxury" cars.
   - Separate the dataset into "Standard" and "Luxury" subsets.
   - Perform a bootstrap sample (random sample with replacement) on the "Luxury" subset so that its row count matches the *exact* row count of the "Standard" subset. 
   - **Crucial**: Use `random_state=42` when sampling the "Luxury" subset in pandas (i.e., `df.sample(n=..., replace=True, random_state=42)`).
   - Concatenate the original "Standard" subset and the newly bootstrapped "Luxury" subset into a single dataframe.

3. **Output**:
   - Save the final combined dataframe to `/home/user/processed_cars.csv` (without the index).
   - Calculate the overall mean `price` of this final combined dataset. Save this single numeric value, rounded to exactly 2 decimal places, into `/home/user/metrics.txt`.

Ensure your script runs successfully and creates the required output files.
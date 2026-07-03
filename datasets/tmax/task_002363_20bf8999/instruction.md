You are a data engineer building an ETL pipeline in Rust. A junior developer has created a preliminary data processing pipeline that reads a 2D dataset, applies Min-Max scaling, splits the data into a training set and a testing set, and then performs a simple similarity search. 

However, during a code review, you noticed a classic data science bug: **Data Leakage**. The junior developer applied the Min-Max scaler on the *entire* dataset before splitting it. This means information from the test set's distribution (its minimums and maximums) leaked into the training set's features.

Your task is to fix the ETL pipeline.

**System Setup & Initial State:**
- A Rust project is located at `/home/user/etl_pipeline`.
- The dataset is located at `/home/user/data/dataset.csv`.
- The dataset has 10 rows and 2 columns (Feature 1 and Feature 2). 

**Your Objective:**
1. Modify the Rust code in `/home/user/etl_pipeline/src/main.rs` to fix the data leakage.
2. The split should remain the same: the first 8 rows (indices 0 to 7) are the training set, and the last 2 rows (indices 8 to 9) are the testing set.
3. You must calculate the Min and Max for Feature 1 and Feature 2 **strictly using only the training set**.
4. Apply these training-derived Min/Max values to scale *both* the training set and the testing set. (Formula: `scaled_value = (value - train_min) / (train_max - train_min)`).
5. After scaling, find the nearest neighbor in the *training set* for the *first sample of the testing set* (which was originally row index 8). Use the standard Euclidean distance on the scaled features.
6. Write the result to a text file at `/home/user/nearest_neighbor.txt`. The file must contain exactly one line with the 0-based index of the nearest neighbor (relative to the training set array, i.e., 0 to 7) and the Euclidean distance formatted to exactly 4 decimal places, separated by a comma.

Example expected format for `/home/user/nearest_neighbor.txt`:
`3,0.4512`

Compile and run your Rust program to generate the required output file.
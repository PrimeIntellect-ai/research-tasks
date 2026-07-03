You are a data scientist reviewing a dataset processing pipeline written in Rust. We have a Rust project located at `/home/user/dataset_processor`. The project simulates splitting a dataset into training and testing sets, normalizing the data (using z-score standardization: subtracting the mean and dividing by the standard deviation), and then calculating a dummy evaluation metric (the sum of the normalized test set values).

However, there is a data leak in the pipeline! The current implementation calculates the `mean` and `standard deviation` using the *entire* dataset (both train and test splits) before splitting them. This causes the test data's distribution to influence the normalization parameters, violating the independence of the test set.

Your task is to:
1. Examine the code in `/home/user/dataset_processor/src/processor.rs`.
2. Fix the `process_data` function so that it splits the data *first*. The `mean` and `std` must be calculated strictly on the `train` split. Then, apply these parameters to normalize the `test` split.
3. Ensure that `cargo test` passes successfully (the tests have been configured to check for the correct numerical accuracy without the data leak).
4. Run the project using `cargo run` and redirect its standard output to `/home/user/result.txt`.

Ensure your fix correctly avoids the data leak and that the final output in `/home/user/result.txt` reflects the correct dummy metric based purely on the training set's normalization parameters.
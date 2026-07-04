You are an ML Engineer tasked with writing a Rust application to prepare training data and evaluate a basic K-Nearest Neighbors recommendation pipeline. 

A previous engineer attempted this but accidentally introduced a "data leak" where the test data influenced the normalization step, ruining the pipeline's reproducibility and validity. You need to build a correct version from scratch.

You are provided with three files:
1. `/home/user/features.csv`: Contains user features. Columns: `user_id,f1,f2,f3`
2. `/home/user/labels.csv`: Contains the target interaction labels for the users. Columns: `user_id,label` (Labels are integers).
3. `/home/user/test_ids.txt`: Contains a list of `user_id`s (one per line) that belong to the test set. All other users belong to the training set.

Your task is to write a Rust program in `/home/user/recommender` (using `cargo new recommender`) that does the following:
1. **Multi-source joining**: Join the features and labels on `user_id`. Note: Some users in `features.csv` might not have labels in `labels.csv`. Only keep users that exist in both files.
2. **Train/Test Split**: Separate the joined data into a training set and a test set based on the IDs in `test_ids.txt`.
3. **Data Normalization (Avoid Data Leaks!)**: Calculate the mean and standard deviation for each feature (`f1`, `f2`, `f3`) using **strictly the training set**. Then, standardize (Z-score normalization: `z = (x - mean) / std`) the features for both the training and test sets using the training set's statistics. 
   *(Note: Use population standard deviation or sample standard deviation, but be consistent. For this task, use the sample standard deviation: divide by N-1).*
4. **Similarity Search**: For each user in the test set, find the single most similar user (1-Nearest Neighbor) in the training set using the **Euclidean distance** on the normalized features. If there is a tie, pick the user with the lowest `user_id`.
5. **Prediction**: Predict the test user's label as the label of their nearest neighbor.
6. **Output**: Write the predictions to `/home/user/predictions.csv` with the header `user_id,predicted_label`, sorted by `user_id` in ascending order.

Requirements:
- You must write the solution in Rust. You may use external crates like `csv` or `serde` if you wish, but the standard library is sufficient.
- Build and run your Rust program to generate `/home/user/predictions.csv`.
- Make sure to carefully prevent data leaks during the Z-score normalization phase.
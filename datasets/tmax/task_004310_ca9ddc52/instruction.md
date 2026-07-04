You are tasked with helping a researcher organize their dataset of paper recommendations and implement a simple collaborative filtering system in Rust. The researcher has a pipeline that was supposed to process user ratings, but it silently introduced missing values when joining datasets, leaving gaps in the ratings matrix.

Your goal is to write a Rust program that completes the data pipeline, performs a similarity search, and uses a basic hyperparameter tuning step to recommend papers.

You have three datasets located in `/home/user/data/`:
1. `users.csv`: Contains `user_id` and `department`.
2. `train_ratings.csv`: Contains `user_id`, `paper_id`, and `rating` (1 to 5). Some ratings are missing (represented by empty strings) because of a previous buggy join.
3. `val_ratings.csv`: Contains `user_id`, `paper_id`, and `rating`. These are the ground-truth values for tuning.

You must create a Rust project in `/home/user/recommender` and write a program that does the following:
1. **Multi-source Data Joining & Preprocessing**: Read `train_ratings.csv`. For any missing rating (empty string), replace it with that specific user's average rating (calculated from their existing valid ratings in `train_ratings.csv`). If a user has no valid ratings at all, default their average to `3.0`.
2. **Linear Algebra & Similarity**: Construct a dense User-Paper matrix. The rows should represent `user_id` (sorted numerically from lowest to highest) and columns should represent `paper_id` (sorted numerically from lowest to highest). Calculate the cosine similarity between every pair of users based on this matrix.
3. **Similarity Search & Recommendation**: To predict a user's rating for a specific paper, find the `K` most similar other users (excluding the user themselves) using the cosine similarity. The predicted rating is the average of the ratings given to that paper by those `K` similar users. If none of the `K` most similar users rated the paper in the training set (or if their imputed rating is used, treat it as their rating), just average whatever values exist in the dense matrix for those `K` users. 
   *(In case of a tie in cosine similarity, prefer the user with the smaller `user_id`)*.
4. **Cross-validation / Hyperparameter Tuning**: Evaluate `K=1`, `K=2`, and `K=3`. For each `K`, calculate the Mean Squared Error (MSE) of your predictions against the actual ratings in `val_ratings.csv`. Select the `K` that yields the lowest MSE.
5. **Reporting**: Write the best `K` and the final predictions for the validation set using that best `K` to `/home/user/result.txt` in the following exact format:

```
Best K: [K]
Predictions:
[user_id],[paper_id],[predicted_rating rounded to 2 decimal places]
... (sorted by user_id ascending, then paper_id ascending)
```

You have access to the standard Rust toolchain. You may create the `Cargo.toml` and use crates like `csv`, `serde`, and `ndarray` if you wish. 

Ensure your final code is compiled and run, and that `/home/user/result.txt` is generated successfully.
You are a data analyst tasked with fixing a data leakage issue in a recommendation system's feature engineering pipeline, using only standard Linux command-line tools (Bash, awk, sed, sort, etc.).

Currently, our pipeline processes user interaction data to calculate item popularity features. However, there is a data leak: the item average ratings are being calculated over the *entire* dataset before splitting it into chronological train and test sets. This causes future test data to leak into the training features.

Your objective is to build a new bash script, `/home/user/pipeline.sh`, that correctly processes the raw dataset `/home/user/ratings.csv` without leakage. 

The `ratings.csv` file has a header and uses the format: `user_id,item_id,rating,timestamp`.

Your script `/home/user/pipeline.sh` must perform the following steps when executed:
1. **Chronological Split**: Split `ratings.csv` (excluding the header) into a training set and a test set. 
   - Training set: All rows where `timestamp` <= 1620000000.
   - Test set: All rows where `timestamp` > 1620000000.
2. **Global Train Mean**: Calculate the global average rating across *all* rows in the training set.
3. **Item Train Mean**: Calculate the average rating for *each specific item_id*, using *only* the training set.
4. **Feature Application**: Create two new files: `/home/user/train_features.csv` and `/home/user/test_features.csv`.
   - Both files must include the original header, with a new column appended: `user_id,item_id,rating,timestamp,item_mean`
   - For every row in the train and test sets, append the `item_mean` (the average rating for that `item_id` calculated in step 3).
   - **Crucial**: If an `item_id` in the test set does *not* exist in the training set (a cold-start item), use the Global Train Mean (from step 2) as its `item_mean`.
   - Format all appended averages to exactly 2 decimal places (e.g., `3.50`).

Your script must be executable (`chmod +x /home/user/pipeline.sh`) and self-contained. You should run your script to ensure the output files are generated correctly.
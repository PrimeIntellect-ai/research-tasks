You are a Machine Learning Engineer preparing tabular data for a user recommendation system. You have inherited a data preparation script that has a critical flaw: it leaks information from the test set into the training set during the imputation and scaling phases.

Your workspace contains:
1. `/home/user/data/raw_users.csv`: A raw dataset of user profiles.
2. `/home/user/src/pipeline.py`: A faulty Python script that processes this data.
3. `/home/user/requirements.txt`: Required dependencies.

Your task is to fix the pipeline, implement missing functionality, and run a similarity search on the cleaned data.

Perform the following steps:
1. **Environment Setup**: Install the packages listed in `/home/user/requirements.txt`.
2. **Fix the Data Leak**: Modify `/home/user/src/pipeline.py`. The current script applies `SimpleImputer` and `StandardScaler` to the *entire* dataset before splitting it. You must rewrite the script so that `train_test_split` (with `test_size=0.25`, `random_state=42`, and no shuffling) happens **first**. All imputers and scalers must be `fit` strictly on the training set, and then used to `transform` both the train and test sets.
3. **Add Outlier Handling**: Before imputation, you must handle outliers in the `income` column. Clip the `income` values to the 5th and 95th percentiles. **Crucially**, these percentiles must be calculated *only* on the training set, and then applied to both the train and test sets.
4. **Save the Processed Data**: The script must save the final processed training and testing DataFrames (with columns `user_id`, `age`, `income`, `activity_score` - where `user_id` remains unscaled/unimputed) to `/home/user/data/processed/train.csv` and `/home/user/data/processed/test.csv` (without indices).
5. **Similarity Search**: After saving the data, write a new script `/home/user/src/similarity.py` that loads the processed train and test sets. It should find the single most similar user in the *training* set to the *first* user (index 0) in the *test* set. Use Cosine Similarity computed across the `age`, `income`, and `activity_score` features. Write the integer `user_id` of this most similar training user to `/home/user/data/processed/most_similar_user.txt`.

Ensure all directories exist. You may run the scripts from the terminal to produce the final outputs.
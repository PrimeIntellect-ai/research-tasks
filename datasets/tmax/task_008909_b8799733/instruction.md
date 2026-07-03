You are tasked with building a simple ETL and similarity search pipeline in C++ for a machine learning setup. 

You have been provided with two datasets:
- `/home/user/train.csv`
- `/home/user/test.csv`

Both files have a header `id,f1,f2,f3` and contain numerical data.

Your goal is to write a C++ program at `/home/user/etl_pipeline.cpp` that performs the following steps:
1. **Data Ingestion**: Read both CSV files.
2. **Feature Engineering (Standardization)**: Calculate the mean and standard deviation for each feature (`f1`, `f2`, `f3`) strictly using ONLY the records from `train.csv`. This is crucial to prevent "data leakage" from the test set. Standardize both the train and test records using these training statistics. The formula is `z = (x - mean) / std`. If the standard deviation for a feature is 0, use 1 instead to avoid division by zero. Use sample standard deviation (N-1).
3. **Similarity Search**: For each record in the test set, find the single closest record in the train set using Euclidean distance based on the standardized features. In case of a tie, choose the training record with the smaller `id`.
4. **Export**: Write the results to `/home/user/closest.csv` with a header `test_id,closest_train_id`. Each subsequent line should map a test `id` to its nearest train `id`.

Compile your C++ program using `g++ -O3 -std=c++17 /home/user/etl_pipeline.cpp -o /home/user/etl_pipeline` and execute it to generate the output file.
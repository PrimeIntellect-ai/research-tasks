You are a Machine Learning Engineer preparing a text-based tabular dataset for a new embedding model. 

You have been given a C++ script at `/home/user/prepare_data.cpp` that reads a small dataset from `/home/user/data.csv`. The script performs an ETL pipeline: it tokenizes the text into integer IDs to prepare for embeddings, mean-centers a numerical feature, and then splits the data into a training set (first 80%) and a test set (last 20%). Finally, it outputs `train_features.txt` and `test_features.txt`.

However, the current implementation has a critical flaw: a **data leak**. The vocabulary dictionary and the mean of the numerical feature are being computed over the *entire* dataset (both train and test) before the split. 

Your task is to fix `/home/user/prepare_data.cpp` so that:
1. The vocabulary and the feature mean are computed **only** on the training set (the first 8 rows).
2. The vocabulary assigns integer IDs starting from `1` based on the order of first appearance in the training set.
3. Any out-of-vocabulary (OOV) words encountered in the test set must be assigned the ID `0`.
4. The test set's numerical features must be centered using the training set's mean.

The output format for both `train_features.txt` and `test_features.txt` must remain:
`id,token_ids_space_separated,centered_feature`

Recompile the script using `g++ -O3 prepare_data.cpp -o prepare_data` and run it to produce the correct output files. Do not change the file paths or output formatting.
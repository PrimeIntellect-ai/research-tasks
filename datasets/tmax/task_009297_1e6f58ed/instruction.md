You are an AI assistant helping a data science researcher who is organizing datasets. 

The researcher suspects that a data leakage issue occurred during the feature engineering pipeline of their embedding models. Specifically, they believe someone mistakenly used `fit_transform` on the test datasets instead of just `transform`, meaning the test datasets were independently centered to have a mean of 0.000 for their feature dimensions, rather than being centered using the training dataset's mean.

You have been given three test datasets containing pre-computed embedding vectors:
1. `/home/user/datasets/test_split_alpha.csv`
2. `/home/user/datasets/test_split_beta.csv`
3. `/home/user/datasets/test_split_gamma.csv`

Each dataset is a CSV file with a header row `id,emb_1,emb_2,emb_3`. 

Your task is to:
1. Use standard bash utilities (e.g., `awk`, `sed`, `bc`) to calculate the arithmetic mean of the `emb_1` column (the second column) for each dataset. Ignore the header row.
2. Identify which dataset has an `emb_1` mean that is numerically equal to zero (an absolute value strictly less than `0.0001`). This indicates the dataset was improperly zero-centered on itself (a data leak).
3. Write the exact filename (just the base name, e.g., `test_split_alpha.csv`) of the leaked dataset to a file at `/home/user/leak_report.txt`.

Do not write any extra text to `/home/user/leak_report.txt`. It should contain only the filename.
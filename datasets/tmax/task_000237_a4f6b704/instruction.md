You are a researcher organizing a dataset of embeddings. You have written a Rust program to process a dataset of 100 items, each represented by a 5-dimensional numerical vector. 

The current program reads the data, centers the features by subtracting the column means, and then splits the data into a training set (first 80 rows) and a test set (last 20 rows). Finally, it calculates the sum of all elements in the transformed test set.

However, your code has a classic **data leakage** bug: you are computing the column means over the *entire* dataset before splitting it. This means information from the test set is leaking into the training set's transformation phase.

Your task is to:
1. Navigate to `/home/user/dataset_organizer`.
2. Modify `src/main.rs` to fix the data leakage. You must split the data into the training set (first 80 rows) and test set (last 20 rows) *before* performing any centering.
3. Compute the column means using *only* the training set.
4. Subtract these training means from both the training set and the test set.
5. Calculate the sum of all elements in the transformed test set.
6. Run your program and save the printed output exactly to a file named `/home/user/dataset_organizer/test_sum.txt`. The output should be formatted precisely as: `Test sum: <value>`, where `<value>` is rounded to 4 decimal places.

To get started, review the existing code in `/home/user/dataset_organizer/src/main.rs` and the data in `/home/user/dataset_organizer/data/embeddings.csv`.
You are tasked with fixing a data preprocessing pipeline written entirely in Bash. 

We have a dataset at `/home/user/dataset.csv` with 1000 rows and 5 columns (comma-separated, no header).
Currently, we have a script `/home/user/pipeline.sh` that is supposed to prepare this data for a downstream classification model. However, the script has two major issues:
1. **Data Leakage:** It computes the Min-Max scaling for column 3 over the *entire* dataset before splitting into train and test sets. This leaks information from the test set into the training set.
2. **Poor Feature Selection:** Column 5 is heavily corrupted and needs to be completely dropped.

Your task:
Modify or rewrite `/home/user/pipeline.sh` to correctly process the dataset. The script must execute when called as `bash /home/user/pipeline.sh` and perform the following exact steps:
1. Split the dataset. The first 800 rows should belong to the training set, and the remaining 200 rows belong to the test set. (Maintain the original order, do not shuffle).
2. For the training set, find the minimum and maximum values of column 3.
3. Apply Min-Max scaling to column 3 for *both* the training and test sets using the minimum and maximum values found *only* in the training set. The formula is `(value - min) / (max - min)`. Format the scaled value to 4 decimal places using standard rounding (e.g., `printf "%.4f"`).
4. Drop column 5 from both sets. The output should only contain columns 1, 2, 3 (scaled), and 4.
5. Save the processed training set to `/home/user/train_processed.csv`.
6. Save the processed test set to `/home/user/test_processed.csv`.

Once you have fixed the script, execute it to generate the output files. We will verify the correctness of `/home/user/train_processed.csv` and `/home/user/test_processed.csv`.
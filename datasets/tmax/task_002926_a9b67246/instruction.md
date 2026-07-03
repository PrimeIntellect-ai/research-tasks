You are an AI assistant helping a data science researcher set up an analysis environment and organize datasets. The researcher has written a Bash script to process a dataset of text documents, extract features (like word counts), normalize them, and split them into a training and testing set. 

However, there is a **data leakage** bug in the pipeline, similar to calling `fit_transform` on the entire dataset before splitting.

Here are the requirements:

1. **Environment Setup & Dataset:**
   The dataset is located at `/home/user/data/documents.csv`. The CSV has three columns: `id`, `text`, and `label` (numeric). The first row is the header.
   The researcher's script is located at `/home/user/prepare_dataset.sh`. It currently calculates the maximum word count across the *entire* dataset to normalize the word count feature. 

2. **Fixing the Leak:**
   Modify `/home/user/prepare_dataset.sh`. 
   - The script must first split the data (80% train, 20% test). Keep the current splitting logic (first 80% rows after header for train, remaining for test).
   - The normalization parameter (`MAX_WORDS`, which is the maximum number of words in a document's `text` field) must be computed **ONLY from the training set**.
   - Use this training `MAX_WORDS` to normalize both the training set and the testing set.
   - The output files should be written to `/home/user/data/train_normalized.csv` and `/home/user/data/test_normalized.csv`. They should contain no header, and consist of three space-separated columns: `id`, `normalized_word_count`, `label`.

3. **Validation & Covariance Analysis:**
   Write a new Bash script at `/home/user/validate.sh`.
   - This script must read `/home/user/data/test_normalized.csv`.
   - It must compute the **population covariance** between the `normalized_word_count` (Column 2) and the `label` (Column 3).
   - Use `awk` to perform this calculation.
   - The formula for population covariance is: `Cov(X,Y) = (Sum(X_i * Y_i) / N) - (mean_X * mean_Y)`
   - The script should save the computed covariance (rounded to 4 decimal places) to a file named `/home/user/covariance_result.txt`.

Ensure the scripts are executable. Run `/home/user/prepare_dataset.sh` and then `/home/user/validate.sh` to generate the final output.
You are acting as a Data Scientist preparing a messy text-based dataset for downstream modeling. You need to write a Go program to process customer reviews, handle anomalies, tokenize text, and perform a basic correlation analysis.

You have been provided with a raw dataset at `/home/user/raw_reviews.csv` with the following columns:
`ReviewID,Text,Rating,Price`

Your task is to write a Go application in the directory `/home/user/cleaner` that performs the following steps:

1. **Environment Setup**: Create a Go module named `cleaner` in `/home/user/cleaner`. You may use third-party packages like `gonum.org/v1/gonum/stat` if you wish.
2. **Missing Value and Outlier Handling**: Read the CSV and filter out invalid rows.
   - Drop rows where `Text` is entirely empty or missing.
   - Drop rows where `Rating` is strictly less than 1 or strictly greater than 5.
   - Drop rows where `Price` is strictly less than 0.
3. **Tokenization and Dataset Preparation**: For the remaining valid rows:
   - Convert the `Text` to lowercase.
   - Remove all periods (`.`) and commas (`,`).
   - Tokenize the text by splitting on single spaces.
   - Count the number of tokens (words) for each review.
   - Save this cleaned dataset to `/home/user/cleaned_reviews.csv`. It should have the headers: `ReviewID,Text,Rating,Price,TokenCount`. (The `Text` in this output should be the raw text from the input, not the tokenized version).
4. **Correlation Analysis**: Calculate the Pearson correlation coefficient between the `TokenCount` (X) and the `Rating` (Y) across all the valid rows.
5. **Output Validation**: Write the computed correlation coefficient to `/home/user/correlation.txt`, formatted to exactly 4 decimal places (e.g., `-0.1234` or `0.5670`).

Make sure your Go code builds and runs successfully. The final verification will check the contents of `/home/user/cleaned_reviews.csv` and `/home/user/correlation.txt`.
You are an AI assistant helping a researcher process and track datasets.

The researcher has a set of raw text files located in `/home/user/raw_data/`. 
You need to write and execute a Go program at `/home/user/tokenize_dataset.go` that performs tokenization, dataset preparation, and simple experiment tracking.

Your Go program must do the following:
1. Read all `.txt` files in the `/home/user/raw_data/` directory.
2. Tokenize the text from all files combined. The tokenization rules are:
   - Convert all text to lowercase.
   - Extract only valid alphabetic tokens. A valid token is defined as any contiguous sequence of the English letters 'a' through 'z' (i.e., matching the regular expression `[a-z]+`).
3. Calculate the following metrics across the entire dataset:
   - `TotalFiles`: The number of `.txt` files read.
   - `TotalTokens`: The total number of valid tokens extracted across all files.
   - `UniqueTokens`: The number of unique valid tokens across all files.
4. Append the results as a single line to an experiment tracking CSV file located at `/home/user/experiments.csv`. 
   - The line must be formatted exactly as: `Run1,TotalFiles,TotalTokens,UniqueTokens` (e.g., `Run1,5,100,45`). Do not include a header row.

Execute your Go program so that the `/home/user/experiments.csv` file is created and populated.
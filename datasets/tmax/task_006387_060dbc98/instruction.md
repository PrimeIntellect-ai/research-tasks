You are a Machine Learning Engineer preparing a dataset of mathematical equations for a sequence-to-sequence symbolic math model. Your raw data is stored in a CSV file, and you need to build a C++ data transformation pipeline to tokenize these equations, calculate token statistics, and track your data preparation experiment.

The raw data is located at `/home/user/equations.csv` and has a header. Each row contains an `id` and a mathematical `expression`.

Your task is to:
1. Write a C++ program at `/home/user/tokenizer.cpp` that reads the `equations.csv` file.
2. The program must tokenize each mathematical expression according to the following strict rules:
   - A token is either: 
     a) A single mathematical operator or punctuation mark from this set: `+`, `-`, `*`, `/`, `=`, `^`, `(`, `)`
     b) A maximal contiguous sequence of alphanumeric characters (letters `a-z`, `A-Z` and digits `0-9`).
   - All spaces in the original expression must be completely ignored.
   - Example: The expression `2x + 3 = 7` tokenizes to `2x`, `+`, `3`, `=`, `7` (5 tokens).
   - Example: `f(x) = 100 / (x - 5)` tokenizes to `f`, `(`, `x`, `)`, `=`, `100`, `/`, `(`, `x`, `-`, `5`, `)` (12 tokens).
3. The program should output a Tab-Separated Values (TSV) file at `/home/user/tokenized_dataset.tsv`.
   - The TSV must NOT have a header.
   - Each row should have three columns separated by a single tab (`\t`):
     Column 1: `id` (from the input CSV)
     Column 2: The tokenized expression (tokens must be separated by exactly one space).
     Column 3: The total token count for that expression (integer).
4. Compile your C++ program using `g++` and execute it to generate the TSV file.
5. Finally, track this dataset preparation run by appending a single summary line to an experiment tracking log located at `/home/user/experiment_log.txt`. The line must be formatted exactly as:
   `Run_Tokens: <TotalEquations>,<TotalTokens>`
   where `<TotalEquations>` is the number of rows processed (excluding the header), and `<TotalTokens>` is the sum of the token counts across all processed equations. Use bash tools (like `awk`, `tail`, etc.) or your C++ program to compute this and write the log.
You are helping a researcher organize and prepare a dataset for training a natural language processing model. 

The researcher has two raw data files:
1. `/home/user/data/metadata.csv` - Contains metadata about documents. Columns: `doc_id`, `author`, `category`. Note that some rows have missing values for `author` or `category`.
2. `/home/user/data/corpus.jsonl` - Contains the actual text. Each line is a JSON object with keys `doc_id` and `text`.

The `doc_id` values are large identifiers (greater than $2^{53}$). The researcher previously tried joining these datasets using standard data science tools, but noticed that some `doc_id` values were silently corrupted (losing precision) during the join process because the missing metadata values caused the ID column to be upcast to floating-point numbers.

Your task is to write and execute a data processing script (in a language of your choice) to accomplish the following:
1. Join the metadata and corpus datasets on `doc_id` using an inner join.
2. Ensure strict numerical accuracy: The `doc_id` values in the output must identically match the original integer values from the input files without any floating-point approximation.
3. Filter out any joined records where the `author` is missing.
4. Tokenize the `text` of the remaining valid records by splitting strictly on single whitespace characters (` `). 
5. Compute the top 3 most frequent tokens across all valid records.

You must generate the following output files:
- `/home/user/output/clean_dataset.jsonl`: The joined and filtered data. Each line must be a JSON object with keys `doc_id` (as a JSON integer or exact string representation), `author`, `category`, and `text`.
- `/home/user/output/top_tokens.txt`: A text file containing the top 3 most frequent tokens and their frequencies, one per line, in the format `token:frequency` (sorted in descending order of frequency, and alphabetically for ties).

Please create the script, run it, and verify that the outputs are generated correctly.
You are an AI assistant helping a data scientist debug a silent data corruption issue in a data preparation pipeline. 

The data scientist is joining metadata about documents with their primary dataset token IDs. However, they noticed that some token IDs in the output seem to be mathematically altered or point to the wrong token mappings downstream.

The working directory is `/home/user/`.

You are provided with two source files:
1. `/home/user/docs.csv`: Contains `doc_id` and `author`.
2. `/home/user/tokens.csv`: Contains `doc_id` and `token_id`. The `token_id` is a very large 64-bit integer.

The data scientist wrote a script, `/home/user/buggy_join.py`, to perform a left join to add token IDs to the documents. Because not all documents have a token ID, pandas introduces `NaN` for the missing rows. Historically, pandas coerces integer columns with `NaN`s into `float64`. This causes a silent loss of numerical precision for large integers (e.g., values > 2^53), altering their exact values.

Your tasks are:
1. Run the existing `/home/user/buggy_join.py` script to generate `/home/user/bad_output.csv`.
2. Write a corrected Python script at `/home/user/fixed_join.py` that reads the same CSVs, performs the same left join (docs left join tokens), but strictly preserves the exact mathematical values of the `token_id`s. You should leverage pandas' nullable integer data type (`Int64`) or read them as strings.
3. Your script must output the corrected joined dataset to `/home/user/fixed_output.csv` (without the dataframe index).
4. Perform an accuracy comparison between `bad_output.csv` and `fixed_output.csv`. Identify the `doc_id`s where the `token_id` was corrupted (i.e., the mathematical value of the integer in the fixed output does not match the numerical value stored in the bad output, ignoring legitimately missing/NaN values).
5. Write the `doc_id`s of the corrupted rows, one per line, to `/home/user/precision_loss_docs.txt`.

Ensure all output files are placed exactly at the specified paths.
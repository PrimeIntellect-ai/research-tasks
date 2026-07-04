A junior data scientist was trying to aggregate a dataset of transactions, but noticed numerical inaccuracies in the output. The dataset, located at `/home/user/transactions.csv`, contains a column called `transaction_id`. Because some of the rows have empty values for this column, the previous pipeline was parsing the entire column as 64-bit floats (`f64`). 

However, `transaction_id` values are large integers. Some of them exceed $2^{53}-1$, meaning they suffer from silent precision loss when parsed as floats.

Your task is to write a Rust program to perform this aggregation exactly, avoiding any precision loss. 

1. Create a new Rust project in `/home/user/cleaner` (e.g., using `cargo init`).
2. You may use the `csv` and `serde` crates.
3. Read the `/home/user/transactions.csv` file.
4. Process the `transaction_id` column: parse it strictly as an exact 64-bit unsigned integer (`u64`). 
5. Any empty values in the `transaction_id` column should be treated as `0`.
6. Compute the total sum of the `transaction_id` column as a `u64`.
7. Write the final sum (as a simple text string, no newline required) to `/home/user/sum.txt`.

Make sure to run your Rust program so that `/home/user/sum.txt` is successfully generated.
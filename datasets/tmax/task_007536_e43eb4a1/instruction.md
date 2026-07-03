You are a data analyst troubleshooting an ETL pipeline. An ETL job failed halfway through yesterday and was retried, which resulted in duplicate transaction records across two output batches. 

Your task is to clean, merge, and summarize this data into a final report.

You have three input files located in `/home/user/data/`:
1. `/home/user/data/users.csv`: Contains user information.
   - Columns: `user_id,region`
2. `/home/user/data/tx_batch1.csv`: First batch of transactions.
   - Columns: `transaction_id,user_id,timestamp,amount`
3. `/home/user/data/tx_batch2.csv`: Second batch of transactions. Contains some duplicate rows from the first batch due to the ETL retry.
   - Columns: `transaction_id,user_id,timestamp,amount`

Perform the following operations:
1. **Union and Deduplicate**: Combine the two transaction batches and remove any duplicate records. (Duplicate records are identical across all columns and share the same `transaction_id`).
2. **Join**: Join the deduplicated transactions with the `users.csv` data using `user_id`.
3. **Sort**: Sort the merged data by `user_id` alphabetically, and then by `timestamp` in ascending chronological order.
4. **Rolling Statistics**: Calculate a rolling cumulative sum of the `amount` for *each user* based on their chronological transactions.
5. **Stratified Sampling**: Retain only the *first 2* transactions (chronologically) for each user.
6. **Output**: Write the final processed data to `/home/user/final_report.csv`.

The output file must be a CSV file with exactly the following header:
`transaction_id,user_id,region,timestamp,amount,cumulative_amount`

Ensure amounts are formatted to one decimal place (e.g., `10.0`).
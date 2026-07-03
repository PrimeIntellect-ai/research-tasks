You are a Data Engineer building ETL pipelines using shell utilities to process NoSQL document data. 

You have been given two JSON files extracted from a document database:
1. `/home/user/users.json`: Contains user profiles with fields `id` and `name`.
2. `/home/user/transactions.json`: Contains transaction records with fields `tx_id`, `user_id`, `amount`, and `status`.

A junior engineer attempted to write an aggregation pipeline to find high-value users, but their approach accidentally created an implicit cross join (Cartesian product) between users and transactions before filtering, causing massive memory consumption and incorrect totals. 

Your task is to write a highly efficient, correct Bash script that processes these JSON files as an aggregation pipeline. 

Requirements:
1. Create a script at `/home/user/etl.sh` and make it executable.
2. The script must process the JSON files to compute the total spent by each user, performing the equivalent of a NoSQL aggregation pipeline using `jq`.
3. The pipeline must:
   - Filter for transactions where `status` is exactly `"COMPLETED"`.
   - Group the filtered transactions by `user_id` and sum the `amount` to create a `total_spent` field.
   - Join the aggregated totals with the users data to include the user's `name`.
   - Filter the final joined results to keep only users where `total_spent` is **150 or greater**.
   - Sort the results by `total_spent` in **descending** order.
4. The script must export the final result to a CSV file at `/home/user/high_value_users.csv`.
5. The CSV file must include a header row: `user_id,name,total_spent`, followed by the sorted data.

Additionally, assume you are migrating this data to MongoDB. Design the optimal index strategy to support this exact query pipeline (filtering by status, grouping by user_id).
6. Create a file `/home/user/mongo_index.js` containing exactly one valid MongoDB `db.collection.createIndex(...)` command for the `transactions` collection that optimally speeds up the initial match and group stages of this pipeline.

Ensure `/home/user/etl.sh` runs successfully and produces the correct output file.
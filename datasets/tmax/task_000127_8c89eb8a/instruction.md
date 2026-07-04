You are a data analyst tasked with optimizing a slow query pipeline for a large dataset of sales transactions. 

Currently, our system receives hundreds of queries a second to calculate the total spend of specific customers. The raw dataset is located at `/home/user/data/sales.csv` and contains roughly 500,000 rows. The current method of scanning the entire file for every query is causing a CPU bottleneck.

Your task is to design a Bash-based indexing strategy and an optimized query pipeline. 

Specifically, you must do the following:

1. Create a script `/home/user/optimize.sh`. When executed, this script should read `/home/user/data/sales.csv` and create a partitioned "index" in the directory `/home/user/index/`.
   - The indexing strategy: Partition the records into exactly 100 files based on the last 2 digits of the `customer_id` (e.g., a record with customer ID `CUST-12345` should be appended to `/home/user/index/part_45.csv`).
   - Ensure the directory is created if it does not exist, and old index files are cleared out before running.

2. Create a fast query script `/home/user/fast_query.sh`.
   - It should accept exactly one argument: the `customer_id` (e.g., `/home/user/fast_query.sh CUST-12345`).
   - It must leverage the partitioned index you created (meaning it should ONLY read from the specific `part_XX.csv` file that could contain the customer's data, drastically reducing I/O).
   - It should filter the customer's transactions for the category `Electronics` only.
   - It must output a single number: the total sum of the `amount` column for that customer within the `Electronics` category.

**File schema for `sales.csv`**:
`tx_id,customer_id,date,category,amount`
*Example row:* `TX-991,CUST-00942,2023-10-01,Electronics,250.50`

Make sure your scripts are executable. Do not use external database engines (like SQLite or PostgreSQL); you must achieve this using standard Linux core utilities (Bash, awk, grep, etc.).
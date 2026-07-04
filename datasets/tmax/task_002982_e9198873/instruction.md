You are a data analyst working on an e-commerce platform's transaction logs. You have been tasked with building an analytical pipeline in C++ that processes raw CSV transaction data, performs complex window aggregations, and outputs a document-oriented (NoSQL-style) JSON summary.

You have a CSV file located at `/home/user/transactions.csv` with the following columns (no header row):
`transaction_id,user_id,timestamp,category,amount`
(e.g., `101,U1,1620000000,Electronics,250.50`)

Your objective is to write a C++ program at `/home/user/process_data.cpp` that performs the following pipeline:

1. **Database Setup & Import**: Use the SQLite3 C API (`sqlite3.h`) to create an in-memory database. Create a table named `transactions` and read the CSV file, inserting all rows into this table. (You will need to install `libsqlite3-dev` to compile your program).

2. **Window Functions**: Execute a SQL query on the in-memory database that retrieves every row while calculating two new analytical columns using SQL window functions:
   - `running_total`: The cumulative sum of `amount` for each `user_id`, ordered by `timestamp` ascending.
   - `category_rank`: The rank of the transaction's `amount` within its `user_id` and `category` partition, ordered by `amount` descending. (Use `ROW_NUMBER()`).

3. **NoSQL-Style Aggregation Pipeline (in memory)**:
   As you iterate through the SQL result set in your C++ code, transform the relational rows into a set of document-like objects (e.g., structs or maps). Group the documents by `user_id` to aggregate the following:
   - `total_spent`: The maximum `running_total` for the user.
   - `top_categories`: A list of unique `category` names where the user had a `category_rank` of 1.

4. **Output**: Write the final aggregated documents into a JSON file at `/home/user/summary.json`. The JSON should be an array of objects, ordered alphabetically by `user_id`. Each object must exactly match this structure:
   ```json
   [
     {
       "user_id": "U1",
       "total_spent": 500.75,
       "top_categories": ["Electronics", "Books"]
     }
   ]
   ```
   *(Note: The `top_categories` array elements should be sorted alphabetically).*

Constraints & Instructions:
- You may use a standard library or download a single-header library like `nlohmann/json` to assist with JSON formatting.
- Compile your program using `g++ -std=c++17 /home/user/process_data.cpp -o /home/user/process_data -lsqlite3`.
- Execute your program so that `/home/user/summary.json` is generated.
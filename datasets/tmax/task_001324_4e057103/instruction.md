You are a data analyst working with a legacy system that exports data as massive, denormalized CSV dumps. You have been given a CSV file located at `/home/user/data/sales_dump.csv`. 

This file contains flat, denormalized records of e-commerce transactions. The columns are:
`TxnID,UserID,UserEmail,UserRegion,ProductID,ProductName,ProductCategory,Price,Quantity,TxnDate`

Your task is to write a Go program at `/home/user/process.go` that performs the following steps:
1. **Data Model Reverse Engineering**: Parse the CSV and load the data into a local SQLite database at `/home/user/sales.db`. You must normalize the data into three separate tables:
   - `users`: `id` (integer), `email` (text), `region` (text)
   - `products`: `id` (integer), `name` (text), `category` (text)
   - `transactions`: `id` (integer), `user_id` (integer), `product_id` (integer), `price` (real), `quantity` (integer), `txn_date` (text - YYYY-MM-DD format)
2. **Index Strategy Design**: Create appropriate database indexes on the newly created tables to optimize filtering by user region and transaction date, as well as the necessary foreign key joins.
3. **Query Construction**: Write and execute a SQL query against your normalized SQLite database to find the top 3 `ProductCategory` values by total revenue (`price * quantity`) strictly for users in the `EU` region, for transactions that occurred in the third quarter of 2023 (between `2023-07-01` and `2023-09-30` inclusive).
4. **Pipeline Output**: Write the results of this query to a CSV file at `/home/user/report.csv`. The file must have the header `Category,TotalRevenue` (TotalRevenue should be formatted to 2 decimal places) and contain exactly the top 3 categories sorted in descending order of revenue.

You may use `github.com/mattn/go-sqlite3` for the SQLite driver. Initialize the Go module in `/home/user` and run your code to produce the `sales.db` and `report.csv` files.
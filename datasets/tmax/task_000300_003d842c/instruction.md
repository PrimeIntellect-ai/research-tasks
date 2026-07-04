You are a data analyst investigating a transaction processing system that recently locked up. You suspect a circular dependency (a deadlock) occurred between transactions. 

You have been provided with two CSV files exported from the system:
1. `/home/user/transactions.csv` - Contains the dependency graph of transactions.
   Columns: `tx_id`, `waits_for_tx_id`
   (This means `tx_id` cannot complete until `waits_for_tx_id` completes).
2. `/home/user/costs.csv` - Contains the computational cost of each transaction.
   Columns: `tx_id`, `cost`

All `tx_id`s and `cost`s are positive integers. There are fewer than 1,000 unique transactions.
There is exactly **one** circular dependency (cycle) in the dataset.

Your task:
1. Write a C program (`/home/user/detect_deadlock.c`) that reads both CSV files.
2. The program must detect the single circular dependency in the transaction graph.
3. The program must calculate the total combined computational cost of all transactions involved in that cycle.
4. Compile and run your C program to generate a report file at `/home/user/deadlock_report.txt`.

The output file `/home/user/deadlock_report.txt` must contain exactly two lines in the following format:
```
Deadlock IDs: <comma-separated list of IDs in the cycle, sorted in ascending order>
Total Cost: <integer sum of costs>
```

For example, if the cycle involves IDs 15, 8, and 42, and their costs are 10, 20, and 30 respectively, the file should look exactly like:
```
Deadlock IDs: 8,15,42
Total Cost: 60
```
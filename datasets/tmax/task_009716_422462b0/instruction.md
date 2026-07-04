You are a database administrator tasked with analyzing a complex locking issue in a legacy system. The system frequently experiences deadlocks, and you need to identify the most problematic transactions to optimize the queries.

You are given a SQLite database at `/home/user/db_locks.sqlite` with an undocumented schema. It contains three tables containing a snapshot of active transactions, the resource locks they currently hold, and the resource locks they are waiting to acquire.

Your task is to:
1. Reverse engineer the data model to identify which table corresponds to `transactions`, `held_locks`, and `requested_locks`. 
2. Construct a "wait-for" directed graph. A transaction X is "waiting for" transaction Y if X has requested a lock on a resource that Y currently holds. 
3. Perform graph traversal to find all transactions that are part of a deadlock (i.e., they are part of a cycle in the wait-for graph).
4. Calculate a "blocking score" for each transaction. The blocking score is the number of other transactions that are directly waiting on it (i.e., the in-degree of the transaction in the wait-for graph).
5. Filter the results to ONLY include transactions that are involved in a deadlock cycle.
6. Sort these deadlocked transactions descending by their `blocking_score`. If there is a tie, sort them alphabetically by their transaction name (ascending).
7. Paginate/limit the results to output only the top 3 transactions.

Write your final result to `/home/user/deadlock_report.json` in the following exact JSON format:
```json
[
  {
    "transaction_name": "...",
    "blocking_score": 0
  },
  ...
]
```

You should write a Python script to perform this analysis and generate the output file.
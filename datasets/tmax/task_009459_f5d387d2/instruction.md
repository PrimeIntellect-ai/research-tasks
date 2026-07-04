You are a data analyst working with a custom financial network dataset. Your task is to process relational CSV data into an in-memory graph representation using C, compute a graph analytics metric (weighted degree centrality), and output a finalized report. 

First, create the following two dataset files in `/home/user/data/` (create the directory if it doesn't exist):

**`/home/user/data/users.csv`**
```csv
user_id,name
1,Alice
2,Bob
3,Charlie
4,Diana
5,Eve
```

**`/home/user/data/transactions.csv`**
```csv
tx_id,sender_id,receiver_id,amount
101,1,2,50.0
102,1,3,20.0
103,2,4,150.0
104,4,1,10.0
105,3,5,80.0
106,5,2,45.0
107,2,3,10.0
```

Your objective is to write a C program located at `/home/user/analyze_graph.c` that does the following:
1. Reads both CSV files and maps them into an in-memory graph representation. The users are nodes, and the transactions are directed edges with weights (amount).
2. Calculates the "Weighted Degree Centrality" for each user. In this context, Weighted Degree Centrality is defined as the sum of the amounts of all incoming AND outgoing transactions for a user.
3. Sorts the users in descending order based on their Weighted Degree Centrality. If two users have the same centrality, sort them by `user_id` in ascending order.
4. Writes the sorted results to a file at `/home/user/centrality_report.txt`.

The output file `/home/user/centrality_report.txt` must follow exactly this format for each user:
```
<user_id>,<name>,<weighted_degree_centrality>
```
Make sure the centrality amounts are formatted to exactly one decimal place (e.g., `150.0`).

Compile your C program using `gcc /home/user/analyze_graph.c -o /home/user/analyze_graph` and run it to generate the report.
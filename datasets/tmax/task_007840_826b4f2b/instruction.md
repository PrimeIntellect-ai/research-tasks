You are a data engineer tasked with building a lightweight C++ ETL pipeline that integrates data from three disparate sources (simulating relational, document, and graph databases) to compute a cross-representation aggregation.

You have three datasets located in `/home/user/data/`:
1. **`users.csv`**: A CSV file (simulating a relational table) with the header `id,name,region`. 
2. **`transactions.jsonl`**: A JSON-lines file (simulating a NoSQL document store) where each line is a JSON object like: `{"tx_id": "t1", "user_id": 1, "amount": 250.5, "status": "COMPLETED"}`.
3. **`network.edges`**: A space-separated file (simulating a graph database export) representing undirected connections between users, formatted as `user_id_A user_id_B weight`.

Your task is to write a C++ program at `/home/user/etl_processor.cpp` that performs the following:
1. **NoSQL Aggregation**: Parse `transactions.jsonl` and aggregate the total transaction `amount` for each `user_id` where the `status` is strictly `"COMPLETED"`.
2. **Entity Tagging**: Identify "Whale" users. A Whale is defined as a user whose total completed transaction amount is `>= 1000.0`.
3. **Graph Traversal**: Parse `network.edges` to build an undirected graph. For *every* user present in `users.csv`, compute the shortest path distance (based on edge weights) to the *nearest* Whale user. (If a user is a Whale, their distance is 0. If a user cannot reach any Whale, their distance should be -1).
4. **Relational Mapping & Output**: Generate a final CSV report at `/home/user/summary_report.csv` with the exact header `user_id,name,region,total_completed_amount,distance_to_whale`. Order the rows ascending by `user_id`. (Format `total_completed_amount` to 1 decimal place, e.g., `0.0` if no completed transactions).

You must compile your program to `/home/user/etl_processor` and execute it to produce the output file. You may use standard C++ libraries. A single-header JSON parsing library is already provided at `/home/user/json.hpp` (include it via `#include "/home/user/json.hpp"` and use `nlohmann::json` if you wish).

Ensure your final output file strictly matches the specified format.
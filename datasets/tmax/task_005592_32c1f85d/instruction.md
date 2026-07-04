You are acting as a database administrator optimizing a custom in-memory graph database engine written in C++. 

The engine processes concurrent transactions between nodes (users) and records these transactions as graph edges. Recently, the system has been hanging completely due to a classic deadlock scenario caused by concurrent transactions. Additionally, an analytical feature for projecting and materializing graph data is missing.

Your task is to fix the deadlock and implement the missing feature in `/home/user/graph_engine.cpp`.

Here is what you need to do:
1. **Fix the Deadlock:** Look at the `process_transaction(int src, int dst, int amount)` function in `/home/user/graph_engine.cpp`. It locks the source node's mutex and then the destination node's mutex. When two threads concurrently execute transactions in opposite directions, it deadlocks. Implement a lock ordering index strategy (always lock the mutex with the lower node ID first) to prevent this.
2. **Implement Graph Projection:** Complete the `materialize_top_transactions(int min_amount, int limit, int offset)` function. This function must:
   - Filter the global `transactions` vector to only include edges where `amount >= min_amount`.
   - Sort the filtered results descending by `amount`. If amounts are equal, sort ascending by `src` ID, then by `dst` ID.
   - Apply the pagination `limit` and `offset`.
   - Write the resulting projected edges to `/home/user/view.txt`, with each line formatted exactly as: `src,dst,amount`.
3. **Run the Pipeline:** 
   - Compile the code: `g++ -std=c++11 -pthread /home/user/graph_engine.cpp -o /home/user/engine`
   - Execute it: `/home/user/engine`

The `main` function is already set up to launch the concurrent threads, wait for them to finish, and then call `materialize_top_transactions(50, 3, 0)`.

Ensure your C++ code handles edge cases gracefully, such as when the offset is greater than the filtered result size.
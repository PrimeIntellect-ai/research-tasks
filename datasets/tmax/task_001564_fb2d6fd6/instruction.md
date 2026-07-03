You are a data engineer working on an ETL pipeline that processes database transaction logs to detect deadlocks (cycles in the transaction wait-for graph). 

We have a naive C++ implementation that detects deadlocks, but it is unacceptably slow on large datasets. Your task is to write an optimized C++ program to replace it.

1. Review the input dataset at `/app/transactions.csv`. It contains columns: `src_tx,dst_tx,wait_time_ms,tx_type`.
2. There is an image at `/app/graph_rules.png` containing specific ETL filtering rules established by the DB admins. You must apply these rules to filter the edges BEFORE building the graph. (You may use the preinstalled `tesseract` to read it or view it manually).
3. Write an optimized C++ program at `/home/user/fast_detector.cpp` that:
   - Reads `/app/transactions.csv`.
   - Applies the filtering rules from the image.
   - Builds a directed graph of transactions (`src_tx` waiting on `dst_tx`).
   - Identifies all transactions (nodes) that are part of AT LEAST ONE cycle (deadlock).
   - Writes the unique transaction IDs involved in deadlocks to `/home/user/deadlocks.txt`, one per line, sorted alphabetically.
4. Compile your program to `/home/user/fast_detector`.

Your implementation will be evaluated against the provided `/app/naive.cpp` (which outputs to the same format). Your program must produce the exact same correct output but achieve a significant runtime speedup. 

The evaluation metric is the runtime speedup factor: `speedup = naive_runtime / your_runtime`.
To pass, you must achieve a `speedup >= 20.0` and 100% output accuracy.
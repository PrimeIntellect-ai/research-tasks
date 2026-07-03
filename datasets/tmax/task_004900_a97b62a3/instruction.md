You are a data engineer building an ETL pipeline to analyze database transaction logs and detect deadlocks using graph analytics.

We have a historical log of lock acquisitions encoded in a video file located at `/app/historical_locks.mp4`. The video is 10 seconds long, at 1 frame per second. Each frame has a plain text overlay in the center with a comma-separated pair: `TransactionID,ResourceID` representing a lock held by that transaction. 

Your task is to:
1. Extract the initial lock state from the video `/app/historical_locks.mp4`. Every second (from t=0 to t=9), there is a lock record.
2. Write a data processing script `/home/user/etl_pipeline.py` (or any language, but compile it to an executable or provide a wrapper script at `/home/user/etl_pipeline.sh` that we can call directly).
3. The script must accept a single command-line argument: the path to a CSV file containing new lock requests. The CSV has no header and the format: `Timestamp,TransactionID,ResourceID,Action` where Action is either `REQUEST` or `RELEASE`.
4. Your script must process the new requests sequentially on top of the initial state extracted from the video. 
   - A `REQUEST` creates a directed edge from the Transaction to the Resource (waiting), unless the resource is free, in which case it acquires it (Resource to Transaction).
   - A `RELEASE` frees the resource, granting it to the transaction that has been waiting the longest (based on the `Timestamp` of their request).
5. The script must output a strictly formatted JSON to `stdout` containing:
   - `deadlocks`: A list of lists, where each inner list contains the `TransactionID`s involved in a circular wait (deadlock), sorted ascending. The outer list should be sorted lexicographically.
   - `longest_wait`: The `TransactionID` that has been waiting for a resource the longest without timing out, calculated using a window function logic over the pending requests.

The script must be efficient. Design an appropriate schema (e.g., in-memory SQLite) with indexes to quickly resolve waits and cycle detection (graph analytics).

Output Schema Validation: The output must strictly match this JSON schema:
```json
{
  "deadlocks": [[1, 2], [3, 4, 5]],
  "longest_wait": 2
}
```

Ensure your script is executable and handles the inputs correctly. We will test it against a hidden reference implementation using randomized CSV inputs.
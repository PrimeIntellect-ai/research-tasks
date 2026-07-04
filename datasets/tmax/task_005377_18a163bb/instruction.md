You are a Database Reliability Engineer tasked with optimizing our backup validation pipeline. We have a massive amount of automated database backup metadata stored in a local SQLite database at `/home/user/backup_metadata.db`.

Currently, we use a legacy, proprietary backup inspection tool to calculate cross-region backup aggregations, detect redundant chunks, and generate an export file. This tool is a stripped binary located at `/app/legacy_inspector`. It runs very slowly because it does not utilize proper query optimization, missing indexes, and executes sub-optimal N+1 queries under the hood. 

Your task involves the following:
1. **Reverse Engineer the Data Model:** Inspect `/home/user/backup_metadata.db` and the output of `/app/legacy_inspector /home/user/backup_metadata.db` to understand the exact aggregations, joins, and filtering being performed.
2. **Optimize Query Strategy:** Determine the optimal SQL queries (utilizing complex joins, CTEs, or window functions if necessary) that replicate the exact logic of the legacy inspector. You may add indexes to the SQLite database if it helps.
3. **Write a C++ Replacement:** Write a C++ program at `/home/user/turbo_inspector.cpp` that queries the SQLite database, performs any necessary cross-query aggregation in memory (or directly via optimized SQL), and exports the results to a CSV format *exactly* matching the output of the legacy tool.
4. **Build and Run:** Compile your C++ code to `/home/user/turbo_inspector`. Ensure it links against SQLite3 (`-lsqlite3`).

The automated test will evaluate your solution based on two criteria:
1. **Equivalence:** The output of `/home/user/turbo_inspector /home/user/backup_metadata.db` must perfectly match the output of `/app/legacy_inspector /home/user/backup_metadata.db`. Write your output to standard out.
2. **Performance:** Your C++ program must execute at least 15x faster than the legacy binary.

Ensure your code is robust, handles parameterized query construction safely, and properly frees database resources.
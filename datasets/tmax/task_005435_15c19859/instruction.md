You are a Database Administrator working on a custom graph analytics engine backed by a relational database. Recently, concurrent graph updates have been causing severe transaction deadlocks in production. 

To solve this, a senior engineer created a highly optimized C utility that takes our custom graph traversal syntax and generates a deadlock-free SQL transaction block. This utility uses lexicographical sorting of row locks and CTEs for cross-query aggregation.

Unfortunately, the source code for this utility was lost. All we have is the stripped, compiled binary located at `/app/sql_generator`.

We are migrating our entire stack to Go and need to rewrite this utility. 

Your task is to write a Go program at `/home/user/generate_sql.go` that takes exactly the same command-line arguments as `/app/sql_generator` and outputs the exact same SQL strings (character-for-character).

**Input Format:**
The binary takes a single string argument in the format:
`GRAPH_UPDATE path=(A)->(B)->(C) nodes=9,2,5`
(The path length and the number of nodes can vary).

**Instructions:**
1. Execute `/app/sql_generator` with various inputs to understand its behavior and output format. Observe how it handles complex joins, CTE construction, and parameter sorting (to prevent deadlocks).
2. Write your Go implementation in `/home/user/generate_sql.go`.
3. Compile your program to an executable named `/home/user/generate_sql`.
    ```bash
    go build -o /home/user/generate_sql /home/user/generate_sql.go
    ```
4. Ensure your Go program is completely standalone and does not call the C binary.

The automated verification system will run both `/app/sql_generator` and `/home/user/generate_sql` with hundreds of randomly generated `GRAPH_UPDATE` strings and assert that their standard outputs are perfectly identical.
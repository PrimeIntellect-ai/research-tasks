As a compliance officer auditing our internal systems for potential collusion, I need you to analyze a database of employee communications. The SQLite database is located at `/home/user/comms.db`.

The database contains a single table `messages` with the following schema:
`CREATE TABLE messages (msg_id INTEGER, sender_id INTEGER, receiver_id INTEGER, timestamp INTEGER, department TEXT);`

I need you to perform the following tasks:

1. **Index Strategy**: The database is unindexed and queries are slow. First, create a composite index named `idx_dept_time` on the `messages` table to optimize queries that filter exactly by `department` and then by `timestamp` (range queries). Do this directly in the SQLite database.

2. **Analysis Script**: Write a Go program at `/home/user/analyzer.go` that does the following:
   - Connects to `/home/user/comms.db` using `github.com/mattn/go-sqlite3`.
   - Executes a strictly **parameterized query** to fetch all messages where the `department` is exactly `"Trading"` and the `timestamp` is greater than or equal to `1672531200`.
   - Maps the relational results into an in-memory directed graph structure (nodes are employee IDs, directed edges represent a message sent from sender to receiver).
   - Performs a basic graph centrality analysis to find the node with the highest **out-degree** (the employee who *sent* the most messages within this filtered dataset). If there is a tie, pick the lowest `sender_id`.
   - Writes the integer `sender_id` of this highly central flagged user to a file located at `/home/user/flagged_user.txt`.

Ensure your Go script compiles and runs successfully. Initialize the go module in `/home/user` and download the required sqlite3 driver before running your script.
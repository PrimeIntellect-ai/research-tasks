You are a Database Reliability Engineer investigating the storage consumption of our new continuous backup system. You have been given a bare SQLite database file at `/home/user/backups.db` containing undocumented backup job metadata.

Your objective is to find the largest "valid backup chain" by total size in bytes. 

A backup chain consists of a root 'FULL' backup and a sequence of 'INC' (incremental) backups that depend on it. 
However, a chain is only valid as long as the backups succeed. 
Specifically:
1. A valid chain must start with a 'FULL' backup that has a status of 'SUCCESS'.
2. An 'INC' backup is only part of the valid chain if its status is 'SUCCESS' **AND** its direct parent backup is also part of the valid chain. If a backup fails, it and all of its descendants are excluded from the valid chain.

You need to figure out the schema of `/home/user/backups.db`, write a query (using recursive CTEs to traverse the graph of parent-child relationships), and calculate the total size (in bytes) of each valid backup chain.

Once you find the chain with the maximum total size, output its root FULL backup ID and the total size in bytes to a file named `/home/user/largest_chain.txt` in the following format:
`RootID,TotalSizeBytes`

For example:
`42,104857600`

You may use any standard shell tools or write a script in a language of your choice (Python, Bash+sqlite3, etc.) to accomplish this.
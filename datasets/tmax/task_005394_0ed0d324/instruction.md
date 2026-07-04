You are a database reliability engineer tasked with analyzing the backup replication network for a globally distributed database system. The databases replicate backup snapshots to one another, and you need to determine the replication latency and prioritize backup storage management.

You have been provided with two files:
1. `/home/user/replication_graph.csv` - Contains the directed replication links between instances and the network latency in milliseconds. Format: `source_instance,target_instance,latency_ms`
2. `/home/user/backup_sizes.csv` - Contains the current backup size in gigabytes for each instance. Format: `instance_id,backup_size_gb`

Write a Rust program at `/home/user/analyze_backups.rs` and compile it to `/home/user/analyze_backups` using `rustc`. The program must perform the following operations:
1. Parse both CSV files.
2. Compute the shortest replication path (minimum total latency) from the primary instance `db-01` to all other reachable instances (including `db-01` itself, which has 0 latency).
3. Join the resulting shortest latency with the backup size for each instance.
4. Filter out any instance that has a backup size strictly less than 10 GB.
5. Sort the remaining instances descending by backup size. If sizes are equal, sort ascending by `instance_id`.
6. Apply pagination to the sorted results: output exactly Page 2, where the page size is 3 items (i.e., the 4th, 5th, and 6th items in the sorted list).
7. Write the paginated result to `/home/user/report.csv` with the exact header `instance_id,shortest_latency_ms,backup_size_gb` followed by the rows.

You can use the Rust standard library (`std::collections::BinaryHeap`, `std::collections::HashMap`, etc.). Do not use external crates. Assume the CSV files are well-formed and do not contain commas within fields.

After writing and compiling the code, run it so that `/home/user/report.csv` is generated.
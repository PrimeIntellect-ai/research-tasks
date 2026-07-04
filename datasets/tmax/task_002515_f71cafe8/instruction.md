You are assisting a compliance officer in auditing system access. We have two datasets:
1. `/home/user/logs.csv`: A relational export of access logs containing `user_id,resource_id`.
2. `/home/user/perms.csv`: An export from our Graph database (originally queried via Cypher: `MATCH (u:User)-[r:CAN_ACCESS]->(res:Resource) RETURN u.id, res.id, r.granted`) containing `user_id,resource_id,granted_flag`.

We wrote a C program, `/home/user/audit.c`, to process these files and identify compliance violations (where a user accessed a resource but their `granted_flag` in the graph database was `0`). 

However, the program is currently producing millions of false positives. Due to a logical error, it acts like a SQL implicit cross join—it fails to properly map the records between the relational representation and the graph representation, and blindly compares every log entry against every permission entry without joining on the composite key (`user_id` and `resource_id`). Furthermore, the O(N^2) iteration strategy is terribly inefficient for large datasets.

Your task:
1. Identify and fix the bug in `/home/user/audit.c` so that it correctly joins the two datasets (a log entry matches a perm entry ONLY if both `user_id` and `resource_id` match).
2. Optimize the cross-representation mapping (e.g., implement a simple indexing strategy like sorting and binary search, or a hash map) so it runs efficiently.
3. Compile your fixed program to `/home/user/audit`.
4. Run the program to generate a report of all actual violations.
5. Save the output to `/home/user/violations.txt`. The format of this file must be a simple list of violations, one per line, in the format: `user_id,resource_id`. Sort the output alphabetically.

Ensure your compiled program runs cleanly and outputs strictly the missing or denied accesses (where the log exists, but the corresponding permission in `perms.csv` is `0` or does not exist).
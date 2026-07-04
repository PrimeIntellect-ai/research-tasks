You are a database administrator working on optimizing and migrating an old permission system to a new Neo4j graph database.

You have been provided with a flat access log in `/home/user/access_log.csv`. This file contains historical access records in the format:
`user_id,role,resource`

However, the underlying permission schema you are reverse-engineering is Role-Based Access Control (RBAC). The data model rules are:
1. A User has a Role (Relationship: `HAS_ROLE`).
2. A Role grants access to a Resource (Relationship: `CAN_ACCESS`).
3. If ANY record shows a specific `role` accessing a specific `resource`, then THAT ROLE grants access to THAT RESOURCE for ALL users who have that role.

Your tasks:
1. Write a C++ program `/home/user/graph_analyzer.cpp` that parses `/home/user/access_log.csv`, infers the implicit graph schema (User -> Role -> Resource) described above, and computes the result of a specific query.
2. The query you need to run conceptually is: "Find all users who have access to the resource 'PROD_DB' through their roles. Sort the resulting unique `user_id`s in descending order, skip the first 2 results, and then limit the output to the next 3 results."
3. Your C++ program must output the final, paginated `user_id`s to a file at `/home/user/results.txt`. Each line must strictly follow the format: `USER_ID: <id>`.
4. Create a text file `/home/user/query.cypher` containing ONLY the raw Cypher query (`MATCH ... RETURN ... ORDER BY ... SKIP ... LIMIT ...`) that represents this exact operation (assuming nodes `User` with property `id`, `Role` with property `name`, and `Resource` with property `name`). Use the node labels `User`, `Role`, and `Resource` and relationship types `HAS_ROLE` and `CAN_ACCESS`. Do not include `CREATE` or `MERGE` statements in this file, only the `MATCH` query.

Compile and run your C++ program to generate `/home/user/results.txt`. Ensure all files are in `/home/user`.
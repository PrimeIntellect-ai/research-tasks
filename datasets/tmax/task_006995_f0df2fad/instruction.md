You are a data analyst working with communication records. You have been provided with two CSV files containing relational data about users and their messaging habits. Your goal is to write a Rust program that analyzes this data as a graph, extracts the top communicators in a specific department, and translates their data into Cypher queries for a graph database.

The input data will be located at `/home/user/data/`:
1. `/home/user/data/users.csv` (Columns: `id`, `name`, `department`)
2. `/home/user/data/communications.csv` (Columns: `sender_id`, `receiver_id`, `message_count`)

Your tasks are:
1. Create a Rust Cargo project named `graph_analyzer` in `/home/user/`.
2. Write a Rust program that reads the CSV files and builds an in-memory directed graph representation. Nodes are users, and directed edges are communications (weighted by `message_count`).
3. Compute the "out-degree centrality" for each user, defined here as the total sum of `message_count` sent by that user.
4. Filter the results to only include users in the "Engineering" department.
5. Sort the filtered users by their out-degree centrality in descending order, and paginate/limit the results to exactly the top 3 users.
6. Write the names and out-degrees of these top 3 users to `/home/user/top_engineers.txt` in the format: `Name,OutDegree` (one per line).
7. For these top 3 users ONLY, map their data and outgoing edges into Cypher queries. Write these queries to `/home/user/cypher_output.cql`. 
   The Cypher file must contain:
   - First, `CREATE` statements for the top 3 users in the format: `CREATE (:User {id: <id>, name: '<name>', department: '<department>'});` (sorted by out-degree descending).
   - Then, `CREATE` statements for all of their outgoing communication edges in the format: `MATCH (s:User {id: <sender_id>}), (r:User {id: <receiver_id>}) CREATE (s)-[:MESSAGED {count: <message_count>}]->(r);` (sorted first by sender's out-degree descending, then by receiver_id ascending).

Compile and run your Rust program so that the output files (`top_engineers.txt` and `cypher_output.cql`) are generated successfully. Ensure the output formats exactly match the specifications.
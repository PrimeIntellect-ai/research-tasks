You are acting as a data analyst. In your workspace at `/home/user/`, you have two CSV files: `users.csv` and `purchases.csv`. 

There is also a Python script `/home/user/generate_cypher.py` that reads these CSV files and is supposed to generate Cypher graph queries to link users to the items they bought. It writes the queries to `/home/user/relationships.cypher`.

However, the script has a logical bug: it is currently generating an implicit cross join (Cartesian product), creating a `:BOUGHT` relationship between *every* user and *every* purchase, resulting in way too many Cypher queries. 

Your task is to:
1. Identify and fix the logic bug in `/home/user/generate_cypher.py`. The schema relationship should be mapped correctly (a user should only be linked to a purchase if the `user_id` matches).
2. Run the fixed script to generate the correct `/home/user/relationships.cypher` file.

The final `/home/user/relationships.cypher` must contain exactly one Cypher statement per line for the valid relationships, in the exact format:
`MATCH (u:User {user_id: <id>}), (p:Purchase {purchase_id: <id>}) CREATE (u)-[:BOUGHT]->(p);`

Do not modify the CSV files. You only need to fix the Python script and generate the correct output file.
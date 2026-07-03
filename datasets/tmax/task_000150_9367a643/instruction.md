You are a data analyst investigating a potential money laundering network. You have been provided with two CSV files representing a network of users and transactions. 

Your task is to build a robust Bash tool that uses a Graph database and Cypher queries to uncover 2-hop transaction patterns (A -> B -> C) originating from suspicious entities.

You have access to the following files:
1. `/home/user/users.csv`: Contains `user_id,name,age`
2. `/home/user/transactions.csv`: Contains `tx_id,sender_id,receiver_id,amount`

Create a Bash script at `/home/user/find_fraud.sh` that takes two arguments: `<suspicious_user_id>` and `<min_amount>`.

Your script must perform the following actions:
1. Create an isolated Python virtual environment at `/home/user/venv` and install `kuzu` (an embedded graph database).
2. Use an inline Python script (via Heredoc or a temporary file) inside your Bash script to:
   - Initialize a local KùzuDB instance in the directory `/home/user/kuzu_db`.
   - Define the Cypher schema for a `User` node table (with `user_id` as the primary key) and a `Transferred` relationship table.
   - Load the provided CSV files into the database.
   - Execute a parameterized Cypher query to find all "destination" users (C) who received money at the end of a 2-hop path (A -> B -> C), where:
     - The starting node A has `user_id` equal to the provided `<suspicious_user_id>`.
     - BOTH transactions in the path (A->B and B->C) have an `amount` strictly greater than `<min_amount>`.
     - The destination user C is NOT the same as user A.
   - Export the results (just the `name` of user C) to standard output.
3. Your Bash script must capture this output and generate a well-formatted JSON array of these destination user names. 
4. The JSON array must be sorted alphabetically and deduplicated.
5. Save the final JSON output to `/home/user/suspects.json`.

Ensure your script handles dependencies silently (e.g., standard pip install output shouldn't corrupt the final JSON output, which should be the only thing written to `suspects.json`).

Once your script is written, execute it with the parameters `U1005` and `500.00` to generate the `/home/user/suspects.json` file.
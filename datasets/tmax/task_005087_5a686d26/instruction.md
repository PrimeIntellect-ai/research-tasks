You are a data analyst tasked with identifying suspicious financial transaction patterns using standard command-line tools. You have been provided with two CSV files representing a transaction network:

1. `/home/user/nodes.csv`
Columns: `node_id,entity_type,region`
Example: `101,Retail,EU`

2. `/home/user/edges.csv`
Columns: `source_id,target_id,amount,timestamp`
Example: `101,202,1500.50,1620000000`

Your goal is to write a Bash script named `/home/user/analyze_network.sh` that uses `sqlite3` (a standard CLI tool) to process these CSVs, find specific knowledge graph patterns, and output a formatted report. 

The script must perform the following logical operations (you may import the CSVs into a temporary SQLite database to achieve this):
1. **Knowledge Graph Pattern Matching & Complex Joins:** Find all directed transaction paths of length 2 (A -> B -> C) where:
   - Node A has `entity_type` = 'Retail'
   - Node B has `entity_type` = 'Intermediary'
   - Node C has `entity_type` = 'Offshore'
   - The timestamp of the A->B transaction must be strictly LESS than the timestamp of the B->C transaction.

2. **Window Functions:** For each valid A -> B -> C path, calculate the total transaction amount (`amount of A->B` + `amount of B->C`). Then, use a window function to assign a rank to each path partitioned by Node A's `region`, ordered by the total transaction amount in descending order.

3. **Query-to-Pipeline:** The output from the database query must be piped through standard Unix tools (like `awk` or `sed`) to replace any `|` (pipe) delimiters with a comma and format the final output.

The final output must be saved to `/home/user/flagged_paths.csv` with the following exact CSV header:
`region,start_node,mid_node,end_node,total_amount,region_rank`

Only include paths where `region_rank` <= 3. 

Make sure the script has execute permissions and runs successfully without any arguments. Do not hardcode the expected answers; your script must dynamically read the input CSVs.
You are a data engineer tasked with building an ETL pipeline to analyze internal company communications. You need to process raw CSV logs, build a knowledge graph of employee interactions, perform graph analytics to identify key influencers, and save the enriched data into a SQLite database using a Python script.

Here is your task:

1. **Input Data**: You will find two files in `/home/user/raw_data/`:
   - `employees.csv`: Contains `emp_id`, `name`, `department`.
   - `messages.csv`: Contains `msg_id`, `sender_id`, `receiver_id`, `timestamp`.

2. **Pipeline Requirements**:
   Write a Python script at `/home/user/etl_pipeline.py` that performs the following steps:
   - Read the input CSV files.
   - Build a directed graph representing communications. An edge from `sender_id` to `receiver_id` should exist if there is at least one message between them. The weight of the edge should be the total number of messages sent from the sender to the receiver.
   - Calculate the PageRank centrality for every employee in the graph to determine their "influencer score". Use a damping factor (alpha) of `0.85` and the message counts as edge weights. (Hint: `networkx` is highly recommended for this).
   - Find all distinct communication "triangles" (cycles of length 3) in the directed graph. A triangle exists if A sends a message to B, B sends a message to C, and C sends a message to A.
   
3. **Output format**:
   Your script must create a SQLite database at `/home/user/company_analytics.db` with the following two tables:
   - `influencers`: Contains columns `emp_id` (INTEGER), `name` (TEXT), `department` (TEXT), and `influencer_score` (REAL). This table must be the result of a join between the employee metadata and the calculated PageRank scores.
   - `triangles`: Contains columns `emp_a` (INTEGER), `emp_b` (INTEGER), `emp_c` (INTEGER). Each row represents a triangle. To avoid duplicates, for each triangle, ensure `emp_a < emp_b < emp_c`.

Run your script to ensure the `/home/user/company_analytics.db` is successfully generated and populated.
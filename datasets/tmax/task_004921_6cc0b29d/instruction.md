You are a data analyst given an export of internal company interactions. Your goal is to process these generic CSV files, reverse engineer an implicit social graph, materialize it into an SQLite database, apply appropriate indexes, and perform window-function analytics to discover key departmental influencers.

The raw data is located in `/home/user/data/`:
1. `employees.csv`: Contains `email` and `department`.
2. `interactions.csv`: Contains `timestamp`, `actor_email`, `target_email`, `interaction_type`, and `metric_value`.

Write a Python script at `/home/user/analyze.py` that does the following:
1. **Database Creation & Loading**: Create an SQLite database at `/home/user/network.db` and load the CSV data into it.
2. **Graph Projection & Materialization**: Reverse engineer the interaction log to materialize a directed graph in a new table named `interaction_graph` with columns `source_email`, `target_email`, and `total_weight`.
   - The `total_weight` for an edge is the sum of all interactions from the source to the target, scaled by type:
     - `email`: weight = 1 * `metric_value`
     - `meeting`: weight = 2 * `metric_value`
     - `code_review`: weight = 5 * `metric_value`
3. **Index Strategy**: Create indexes on `interaction_graph` and your employee tables to optimize joining targets to their departments and grouping by target.
4. **Window Functions & Analytics**: Use a single SQL query leveraging CTEs and Window Functions (`RANK() OVER ...`) to calculate the top 2 influencers per department.
   - An "influencer" is ranked by their total incoming weight from *all* sources.
   - Rank is partitioned by the target's department.
   - In case of a tie in total incoming weight, resolve it by ordering `target_email` alphabetically (A-Z).
5. **Output**: Execute the query and output the results to `/home/user/top_influencers.json`.
   - The JSON should be a list of objects with exactly these keys: `{"department": string, "email": string, "incoming_weight": integer, "rank": integer}`.

You must execute the script so that `/home/user/network.db` and `/home/user/top_influencers.json` are generated successfully.
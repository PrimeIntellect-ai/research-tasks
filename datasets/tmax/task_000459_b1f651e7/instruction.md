You are a database administrator tasked with analyzing cross-system data to identify key influencers in a company's communication network.

The company stores user metadata in a relational SQLite database and interaction logs in a NoSQL-style JSON Lines export. You need to write a Python script that maps data between these representations, constructs an interaction graph, calculates graph metrics, and exports the optimized results.

Here is your environment:
1. Relational Database: `/home/user/users.db` (SQLite3)
   - Table `users`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `department` (TEXT)
2. Document Export: `/home/user/interactions.jsonl` (JSONL)
   - Documents have the format: `{"source_id": <int>, "target_id": <int>, "interaction_type": <string>, "weight": <int>}`

Your tasks are:
1. Install any necessary Python dependencies (e.g., `networkx` is permitted and recommended).
2. Write a Python script at `/home/user/analyze_network.py` that:
   - Reads the interaction documents and constructs a directed graph where an edge exists from `source_id` to `target_id`. The weight of the edge should be the sum of all `weight` values for interactions between that specific source and target.
   - Calculates the weighted in-degree for every node (the sum of the weights of all incoming edges).
   - Maps the graph nodes back to the user metadata in the SQLite database to retrieve the `name` and `department` of each user.
   - Identifies the top 3 users with the highest weighted in-degree. In case of a tie, sort by user `id` ascending.
   - Exports these top 3 users to a JSON file at `/home/user/top_influencers.json` with the exact following format:
     ```json
     [
       {
         "user_id": 123,
         "name": "Alice Smith",
         "department": "Engineering",
         "weighted_in_degree": 450
       },
       ...
     ]
     ```
3. Run your script so that `/home/user/top_influencers.json` is generated successfully.
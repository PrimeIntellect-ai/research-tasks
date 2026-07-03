You are a data analyst investigating a series of financial transactions for potential circular funding loops (similar to deadlocks in concurrent systems, where dependencies form a cycle). 

You have been provided with two CSV files in the `/home/user/data` directory:
1. `/home/user/data/entities.csv`: Contains `entity_id` and `entity_name`.
2. `/home/user/data/transactions.csv`: Contains `source_id`, `target_id`, and `amount`.

Your task is to write a Python script that performs the following graph analytics using the `pandas` and `networkx` libraries:

1. **Graph Construction**: Build a directed graph from the `transactions.csv` file. Treat `source_id` as the source node and `target_id` as the target node. Ignore the transaction amounts for the structure.
2. **Cycle Detection**: Identify all unique simple cycles in the graph that have a length of exactly 3 or exactly 4. 
3. **Graph Analytics (Centrality)**: Calculate the standard Betweenness Centrality for *all* nodes in the entire directed graph. Use the default `networkx.betweenness_centrality` parameters (normalized=True, weight=None).
4. **Filtering and Sorting**: 
   - Filter the nodes to only include those that participate in at least one of the cycles identified in Step 2.
   - Sort these cycle-participating nodes by their Betweenness Centrality in descending order. If there is a tie, sort by `entity_id` in ascending alphabetical order.
5. **Output**: Save the top 3 entities from the sorted list to a JSON file located at `/home/user/cycle_centrality.json`. 

The JSON must be a list of dictionaries with exactly this structure:
```json
[
  {
    "entity_id": "E1",
    "centrality": 0.1234
  },
  ...
]
```
*Note: Round the `centrality` value to exactly 4 decimal places.*

Constraints:
- You must install any necessary Python packages (like `networkx`, `pandas`) yourself.
- Use Python 3.
- The output JSON file must be strictly formatted as requested.
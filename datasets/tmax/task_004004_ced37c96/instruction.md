You are a data analyst working with an extracted knowledge graph representing a social e-commerce platform. The graph data has been dumped into two CSV files located in `/home/user/graph_data/`:
1. `nodes.csv`: Contains graph nodes. Columns: `node_id` (string), `label` (string), `weight` (integer).
2. `edges.csv`: Contains directed relationships. Columns: `source_id` (string), `target_id` (string), `rel_type` (string).

Your task is to write a parameterized Python script that performs a specific knowledge graph pattern match, filters the results, sorts them, applies pagination, and exports the final output.

Create a Python script at `/home/user/query_graph.py` that uses the `argparse` module to accept the following arguments:
- `--action` (string): The relationship type connecting a User to an Item.
- `--min-weight` (int): The minimum weight of the *Item* node (inclusive).
- `--sort-order` (string): Either `asc` or `desc`.
- `--limit` (int): Maximum number of results to return.
- `--offset` (int): Number of results to skip before returning.
- `--output` (string): The file path where the output should be saved.

The script must find all instances of the following directed graph pattern:
`(User) -[action]-> (Item) -[BELONGS_TO]-> (Category)`

Where:
- `(User)` is a node with label `User`
- `(Item)` is a node with label `Item` and a `weight` >= `--min-weight`
- `(Category)` is a node with label `Category`
- `-[action]->` is an edge where `rel_type` matches the `--action` argument
- `-[BELONGS_TO]->` is an edge where `rel_type` is strictly `BELONGS_TO`

For all matched paths, calculate a `path_score` defined as the sum of the User node's weight and the Item node's weight.

Sort the matched paths primarily by the `path_score` (in the direction specified by `--sort-order`), and secondarily by the `User`'s `node_id` in ascending alphabetical order to break ties.

Apply the `--offset` and `--limit` to the sorted results (e.g., if offset is 2 and limit is 3, return the 3rd, 4th, and 5th items).

Finally, save the paginated results to the specified `--output` file in JSON format as a list of dictionaries. Each dictionary must have the following exact keys:
- `user_id`: the node_id of the User
- `item_id`: the node_id of the Item
- `category_id`: the node_id of the Category
- `path_score`: the calculated path score

Ensure your script handles the CSV files purely using standard Python libraries (e.g., `csv`, `json`, `argparse`) or standard pre-installed data manipulation libraries like `pandas`. Do not assume external graph databases are running.
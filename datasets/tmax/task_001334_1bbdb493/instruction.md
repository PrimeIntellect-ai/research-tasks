You are a data analyst working with a hierarchical dataset exported to a CSV file. The file is located at `/home/user/data.csv`.

The CSV contains organizational data with the following columns:
`id,parent_id,name,sales`

Your task is to write a Go program (e.g., at `/home/user/process.go`) that parses this CSV and converts it into a structured JSON document, computing specific hierarchical and analytical fields along the way.

Specifically, your Go program must read `/home/user/data.csv` and write a JSON array of objects to `/home/user/result.json`. 

Each object in the output JSON array must contain the following keys:
- `id` (integer): The ID of the node.
- `name` (string): The name of the node.
- `sales` (integer): The sales value of the node.
- `path` (array of strings): The hierarchical path from the root node down to this node (inclusive). For example, if "CEO" is the root and "VP" is a child of "CEO", the path for "VP" would be `["CEO", "VP"]`.
- `sibling_rank` (integer): The 1-based rank of this node among its siblings (nodes sharing the exact same `parent_id`), ordered by `sales` descending. In the event of a tie in `sales`, break the tie by ordering by `id` ascending. (Treat the root node as having rank 1 among its empty-parent group).

Additional constraints:
- The output JSON array must be sorted by `id` ascending.
- The root node will have an empty string `""` for `parent_id`.
- Do not use any external Go libraries (only standard library).
- Execute your Go program so that `/home/user/result.json` is successfully created.
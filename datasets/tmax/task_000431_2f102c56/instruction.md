You are a data analyst working on a Linux terminal. You need to process a relational CSV file representing a bipartite graph and project it into a unipartite graph, then convert the output into a specific JSON document format. 

You have been provided with a CSV file at `/home/user/purchases.csv`. 
The file has the following header: `user_id,product_id,timestamp`

Your task is to perform a graph projection and materialization using ONLY standard bash tools (like `awk`, `sort`, `join`, `uniq`, `sed`, `jq`).

Specifically, you need to:
1. **Materialize a User-User co-purchase graph**: Create an edge between two distinct users if they have purchased the SAME product.
2. **Calculate Edge Weights**: The weight of the edge between `user_A` and `user_B` is the total number of DISTINCT products they both purchased.
3. **Filter**: Only keep edges where the weight is STRICTLY GREATER THAN 1 (i.e., they share at least 2 distinct products). 
4. **Format Conversion**: Convert the resulting filtered graph into a JSON array of objects. To ensure no duplicate edges or bidirectional redundancies, always order the user IDs in the output such that `source` is lexicographically less than `target`.
5. **Sort**: The final JSON array must be sorted alphabetically by `source`, then by `target`.

The final output must be saved to `/home/user/co_purchase_graph.json` and must strictly match this schema and indentation (using `jq`'s default pretty-print format):
```json
[
  {
    "source": "u1",
    "target": "u2",
    "weight": 2
  },
  ...
]
```

Constraints:
* Do not use Python, Perl, Ruby, or Node.js. You must use standard Unix/Linux shell utilities (e.g., `bash`, `awk`, `sort`, `uniq`, `join`, `jq`).
* Ignore duplicate `user_id,product_id` pairs in the input (a user buying the same product twice only counts as 1 distinct shared product with someone else).
* Ensure the JSON is properly formatted as a single array containing the edge objects.
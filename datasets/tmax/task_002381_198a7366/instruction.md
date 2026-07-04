You are a data analyst tasked with processing a lightweight property graph serialized into CSV files. You need to implement a graph pattern matching algorithm using standard Bash utilities (like `awk`, `join`, `grep`, `sort`, etc.) without installing any external graph databases.

You have two files located in `/home/user/`:
1. `/home/user/nodes.csv` - Contains the graph nodes.
   Format: `node_id,node_label,attr1,attr2`
   - For `User` nodes: `node_id,User,name,age`
   - For `Product` nodes: `node_id,Product,name,price`
   - For `Category` nodes: `node_id,Category,name,description`

2. `/home/user/edges.csv` - Contains the directed edges between nodes.
   Format: `source_id,target_id,rel_type,rel_attr`
   - For `PURCHASED` edges: `source_id,target_id,PURCHASED,purchase_date`
   - For `BELONGS_TO` edges: `source_id,target_id,BELONGS_TO,` (rel_attr is empty)

Your task is to write a Bash script at `/home/user/query_graph.sh` that executes the equivalent logic of the following Cypher query:

```cypher
MATCH (u:User)-[r1:PURCHASED]->(p:Product)-[r2:BELONGS_TO]->(c:Category {name: 'Electronics'})
WHERE CAST(p.price AS FLOAT) > 500
RETURN u.id AS user_id, u.name AS user_name, p.id AS product_id, p.name AS product_name, r1.date AS purchase_date
ORDER BY purchase_date DESC
```

Requirements:
- Your script `/home/user/query_graph.sh` must be executable.
- When run, it must read `/home/user/nodes.csv` and `/home/user/edges.csv`.
- It must produce a CSV output file at `/home/user/results.csv`.
- The output file must include a header row: `user_id,user_name,product_id,product_name,purchase_date`.
- The output must be sorted descending by `purchase_date`.
- You may use standard Unix text processing tools (`awk`, `sed`, `grep`, `sort`, `join`, etc.). Do not use Python, Perl, or Ruby for this task.
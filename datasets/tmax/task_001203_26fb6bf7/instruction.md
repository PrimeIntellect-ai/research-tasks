You are a Database Reliability Engineer (DBRE) tasked with managing backup metadata. We are transitioning our relational backup metadata into a graph database format to better analyze schema dependencies across backups.

You have been provided with a custom C program, `/home/user/graph_mapper.c`, which reads relational backup metadata and maps it to a Cypher-like graph query string format. The input data represents backup tables and their foreign key relationships.

However, the C program currently has a critical bug. It produces an implicit cross join, resulting in a massive, incorrect combinatorial explosion of relationships in the output. Instead of linking a table *only* to the foreign keys it actually originates, it links every table to every foreign key in the dataset.

Your tasks are as follows:

1. **Fix the Bug**: Analyze and modify `/home/user/graph_mapper.c` to fix the implicit cross join. A table should only print a `[:REFERENCES]` relationship if the foreign key's `source_id` strictly matches the table's `id`.
2. **Compile and Run**: Compile the fixed C code (name the executable `graph_mapper`) and run it. Redirect the standard output to `/home/user/mapped_graph.txt`. The output must be sorted alphabetically.
3. **Cross-Query Aggregation**: Write a script (bash, awk, or python) to parse your fixed `/home/user/mapped_graph.txt` and calculate the total number of foreign key references per `Backup` ID. 
4. **Summary Report**: Save the aggregated results to `/home/user/backup_summary.csv`. The CSV must have the header `backup_id,fk_count` and the rows must be sorted in ascending order of the `backup_id`.

**Input Files:**
* `/home/user/backup_data/tables.txt` (Format: `id,backup_id,table_name`)
* `/home/user/backup_data/fks.txt` (Format: `source_id,target_id`)
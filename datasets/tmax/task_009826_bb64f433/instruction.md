You are acting as a database administrator. We have an SQLite database at `/home/user/hierarchy.db` that stores a hierarchical file system structure and disk quotas for directories. 

The database contains two tables:
1. `nodes`
   - `id` (INTEGER PRIMARY KEY)
   - `parent_id` (INTEGER) - refers to `id` of the parent directory. NULL for the root.
   - `name` (TEXT) - name of the file or directory.
   - `type` (TEXT) - either 'dir' or 'file'.
   - `local_size` (INTEGER) - size of the node itself (files have large sizes, directories have small overhead sizes).

2. `quotas`
   - `node_id` (INTEGER PRIMARY KEY) - refers to `id` in the `nodes` table.
   - `max_size` (INTEGER) - the maximum allowed rolled-up size for this directory.

Your task is to write a Python script at `/home/user/check_quotas.py` that connects to this database and identifies which directories are exceeding their disk quotas. 

To calculate the "rolled-up size" (total size) of a directory, you must sum its `local_size` with the `local_size` of ALL its recursive descendants (both subdirectories and files). 

The script should:
1. Use a recursive Common Table Expression (CTE) to compute the total rolled-up size for every node.
2. Filter the results to only include directories (`type = 'dir'`).
3. Join the computed total sizes with the `quotas` table.
4. Find directories where the computed total size is strictly greater than `max_size`.
5. Write the violations to a CSV file at `/home/user/violations.csv`.

The CSV file must have no header row, and the columns must be exactly in this order:
`node_id,name,total_size,max_size`

Sort the output by `node_id` in ascending order.
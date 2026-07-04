You are a Database Reliability Engineer (DBRE) managing a complex backup infrastructure. You have exported the metadata of your system's backups into two CSV files located in your home directory:

1. `/home/user/backups.csv`
   Columns: `backup_id`, `timestamp`, `size_mb`, `type`
   `type` is either `FULL` or `INC` (incremental).

2. `/home/user/dependencies.csv`
   Columns: `backup_id`, `parent_id`
   This represents the restoration graph. An incremental backup requires its parent to be restored first. 

Your task is to calculate the total restoration cost for every backup in the system. The "total restoration cost" of a backup is the sum of its own `size_mb` plus the `size_mb` of ALL its recursive ancestors (i.e., the entire chain of dependencies up to the root `FULL` backup). 

Write a script in the language of your choice that reads the CSV files, traverses the graph dependencies to compute the cumulative sizes, and outputs a summary CSV file. 

The output file must be written to: `/home/user/restore_costs.csv`
It must contain exactly the following columns, with a header row, sorted by `cost_rank` ascending:
`backup_id,total_restore_size_mb,cost_rank`

The `cost_rank` must be calculated using a dense ranking window function over the `total_restore_size_mb` in descending order (the largest total size gets rank 1). If there is a tie in size, break the tie by sorting `backup_id` in ascending alphabetical order.
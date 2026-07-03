You are a data engineer debugging and extending a local ETL pipeline. 

In `/home/user/`, there is a broken bash script named `etl_runner.sh` that attempts to concurrently load two CSV files (`transactions1.csv` and `transactions2.csv`) into a SQLite database (`graph.db`) containing a table named `edges (source TEXT, target TEXT, weight INTEGER)`. 
Currently, the concurrent execution causes a "database is locked" error (a form of deadlock in SQLite).

Your tasks are:

1. **Fix the ETL pipeline:** 
   Modify `/home/user/etl_runner.sh` so that both files are loaded successfully into `graph.db` without lock errors. You may achieve this by optimizing the SQLite configuration (e.g., enabling WAL mode) or by adjusting how the concurrent jobs are executed, as long as all data from both CSVs ends up in the `edges` table. Run the script to generate the database.

2. **Graph Analytics & Result Processing:**
   Create a new bash script at `/home/user/process_results.sh` that queries `graph.db` to perform the following:
   - Calculate the "out-degree weight" (the sum of `weight` for all outgoing edges) for every `source` node.
   - Filter the results to include only nodes where the out-degree weight is greater than 50.
   - Sort the results in descending order by out-degree weight. If there is a tie, sort alphabetically by the `source` node name.
   - Paginate/limit the results to retrieve only the top 3 nodes.
   
   The script must write the output to `/home/user/report.txt` exactly in this format:
   ```
   Node: [source_name], Weight: [total_weight]
   Node: [source_name], Weight: [total_weight]
   ...
   ```
   Finally, your script must perform a cross-query aggregation to calculate the sum of the weights of *only those top 3 nodes*, and append it as the final line to `/home/user/report.txt` in this format:
   ```
   Total Top 3 Weight: [sum]
   ```

Make sure to run your scripts so that `/home/user/graph.db` and `/home/user/report.txt` are populated in their final state.
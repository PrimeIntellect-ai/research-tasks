You are a data engineer optimizing an ETL pipeline. You have been provided with an export of database tables and a query execution plan for a notoriously slow transformation query.

Your task is to analyze the database schema and the query plan using standard Bash tools (like `awk`, `grep`, `sed`, `sort`, `uniq`, etc.) to identify the core bottleneck table.

Here is the setup:
1. All table dumps are located in `/home/user/etl_data/tables/` as CSV files. The name of the file (without the `.csv` extension) is the name of the table.
2. The first line of each CSV file contains the column headers.
3. The database uses a strict naming convention for foreign keys: if a table contains a column named `<target_table>_id`, it represents a foreign key referencing `<target_table>`. 
4. The execution plan of the slow query is located at `/home/user/etl_data/query_plan.txt`.

Perform the following steps:
1. **Reverse Engineer the Schema Graph:** Parse the headers of all CSV files to determine the foreign key relationships. Treat the tables as nodes in a directed graph, where an edge exists from Table A to Table B if Table A contains a foreign key referencing Table B.
2. **Graph Analytics:** Calculate the "in-degree" of each table. In this context, the in-degree is the number of *other tables* that contain a foreign key pointing to it.
3. **Query Plan Interpretation:** Extract the names of the tables that are subjected to a `Seq Scan` in the provided `/home/user/etl_data/query_plan.txt` file. The format in the file will look like: `Seq Scan on "table_name"`.
4. **Identify the Bottleneck:** Among the tables that have a `Seq Scan` in the query plan, identify the one with the *highest* in-degree in your schema graph.

Finally, write the name of this single bottleneck table (just the table name, no quotes or extra text) to `/home/user/bottleneck_analysis.txt`. If there is a tie, write the table name that comes first alphabetically.
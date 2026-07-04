You are a data engineer responsible for fixing and finishing an ETL pipeline written in C++.

We have an SQLite database at `/home/user/graph_data.db` that stores an enterprise social graph. The database contains three tables representing users, their departments, and their connections (edges) to other users. 

There is an existing C++ script at `/home/user/etl_pipeline.cpp` that queries this database, aggregates the number of connections per user, and writes the results. However, the script has a few major issues:
1. **Implicit Cross Join Bug**: The SQL query inside the C++ code is generating wildly incorrect connection counts. It uses an implicit cross join between the users and departments tables instead of correctly linking them based on the data model.
2. **Missing Filter**: The pipeline currently retrieves all users. It needs to be modified (either via SQL or in the C++ processing logic) to only output users who have **strictly more than 2** connections.

Your task is to:
1. Reverse engineer the schema of `/home/user/graph_data.db` to understand how users and departments are linked.
2. Install any necessary dependencies to compile a C++ SQLite3 application (e.g., `libsqlite3-dev`, `g++`).
3. Edit `/home/user/etl_pipeline.cpp` to fix the SQL query's join logic so the counts and department names are accurate.
4. Implement the filter so only users with > 2 connections are kept.
5. Compile the C++ program (e.g., `g++ -o /home/user/etl_pipeline /home/user/etl_pipeline.cpp -lsqlite3`).
6. Run the compiled executable, which must output the final data to `/home/user/pipeline_out.csv`.

The output file `/home/user/pipeline_out.csv` must not contain a header, and must contain comma-separated values in the following exact format:
`user_id,user_name,department_name,connection_count`

Ensure the final counts accurately reflect the number of outgoing connections for each user.
You are a data engineer working on an ETL pipeline. You have been provided with a raw data dump from a legacy communication system. The system logs user details and message transactions, but the documentation is lost. 

Your task is to reverse engineer the data model from the raw files, materialize a directed weighted graph representing the communication network, and perform graph analytics to process the results into a final ETL output. All processing must be written in a single C++ program.

The raw data is located in `/home/user/data/`:
1. `/home/user/data/entities.dat`: A header-less CSV containing user information. By inspecting it, you must deduce which column represents the user ID, name, department, and role.
2. `/home/user/data/edges.dat`: A header-less CSV containing message logs. You must deduce the schema, but you know it contains at least: message ID, sender ID, receiver ID, timestamp, and message size in bytes.

Write a C++ program at `/home/user/etl_pipeline.cpp` and compile it to `/home/user/etl_pipeline`.

The program should:
1. Accept three command-line arguments: `<path_to_entities> <path_to_edges> <output_path>`
2. Read the input files and materialize a directed graph in memory where nodes are users and edges represent messages sent from one user to another. 
3. The weight of an edge from User A to User B should be the **total sum of message bytes** sent from A to B across all messages.
4. Calculate the weighted out-degree centrality (sum of outgoing edge weights) for every user.
5. Filter the results to ONLY include users belonging to the `Engineering` department.
6. Write the results to the specified `<output_path>` as a CSV with the header `user_id,weighted_out_degree`. The rows must be sorted in descending order of `weighted_out_degree`. If there is a tie, sort by `user_id` ascending.

When you are done, compile your code using `g++ -O3 -std=c++17 /home/user/etl_pipeline.cpp -o /home/user/etl_pipeline` and execute it to produce `/home/user/etl_results.csv`.
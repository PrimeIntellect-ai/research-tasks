You are a data engineer building the final stage of an ETL pipeline. We extract communication records from NoSQL document stores, convert them into graph representations, and filter out spam/bot networks before they reach our relational analytics data warehouse.

Your task has three parts:

1. **Fix the Vendored Dependency**
   We use the C++ `nlohmann/json` library for parsing. It is pre-vendored at `/app/json-3.11.2`. However, our upstream synchronization script accidentally introduced a bug into the library's main header file, preventing it from compiling. You must locate and fix the perturbation in `/app/json-3.11.2/single_include/nlohmann/json.hpp` so it can be used to compile your code. No internet access is available, so you must use this local package.

2. **Develop the Graph ETL Filter**
   Write a C++ program at `/home/user/etl_filter.cpp` and compile it to `/home/user/etl_filter`. 
   The program must take two command-line arguments: an input directory and an output directory.
   Invocation: `/home/user/etl_filter <input_dir> <output_dir>`
   
   The program must iterate through all `.json` files in `<input_dir>`. Each file represents a communication window (Document representation) and contains an array of objects with `source` and `target` string fields (Relational edge list).
   
   For each file, your program must:
   - Build an undirected, unweighted graph.
   - Compute the **Degree Centrality** of each node.
   - Compute the **Clustering Coefficient** for the graph to detect unnatural patterns.
   - Apply analytical window-like reasoning: A file is considered a "bot ring" (evil) if the graph is a perfect or near-perfect disconnected ring (e.g., all nodes have a degree of exactly 2, and the graph forms a single cycle).
   - *Filter Rule*: If the graph represents a pure bot ring (every node has degree exactly 2 and the graph is connected, OR contains obvious self-loop spam where >50% of edges are self-loops), it must be REJECTED.
   - If REJECTED, do not output anything for that file.
   - If ACCEPTED (clean), write the original JSON array to `<output_dir>/<filename>` exactly as it was.

3. **Verify Against Corpora**
   We have provided two test directories:
   - `/app/data/clean/`: Contains normal, organic communication graphs.
   - `/app/data/evil/`: Contains purely malicious bot-ring graphs and self-loop spam.
   
   Your compiled binary must successfully accept all files from the clean directory and reject all files from the evil directory when run against them. To test your program, process both directories and output the accepted files into `/home/user/output_clean/` and `/home/user/output_evil/` respectively. Ensure your filtering logic perfectly separates the two.

You must build the executable using standard C++17 (`g++ -std=c++17`) and include the fixed vendored JSON header.
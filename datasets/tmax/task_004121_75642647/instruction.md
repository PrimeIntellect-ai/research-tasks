You are acting as a data engineer helping process a graph dataset from CSV files. We have an existing C++ pipeline that is producing incorrect results due to an implicit cross join in the logic (it iterates over all edges naively instead of properly building a graph adjacency list), making it unacceptably slow and generating duplicate/wrong 2-hop paths.

Here is your setup and requirements:
1. **Data Files**: 
   - `/home/user/nodes.csv` (Columns: `node_id`, `label`)
   - `/home/user/edges.csv` (Columns: `source`, `target`, `weight`)
2. **Audio Update**: The product manager left a voice memo at `/app/update.wav`. You must transcribe or listen to this audio file to find out:
   - Three missing edges that must be appended to `edges.csv` before processing.
   - The exact number of top results (pagination limit) we want to output.
3. **The C++ Code**: `/home/user/process_graph.cpp` contains the buggy logic. 
   - Your task is to rewrite or fix this C++ code so that it correctly computes the maximum 2-hop path weight between any two distinct nodes A and C (i.e., paths of exactly length 2: A -> B -> C, where A != C). 
   - The weight of a path is the sum of the edge weights: `weight(A,B) + weight(B,C)`.
   - If there are multiple 2-hop paths between A and C, keep the one with the maximum total weight.
   - The output must be sorted by `total_weight` in descending order, then by `source` ascending, then `target` ascending.
   - Apply the pagination limit specified in the audio file.
4. **Execution & Output**: 
   - Compile your code: `g++ -O3 -std=c++17 /home/user/process_graph.cpp -o /home/user/process_graph`
   - Run the executable. It must write the final results to `/home/user/final_results.csv` with the header `source,target,total_weight`.

Fix the code, integrate the audio instructions, and produce the final CSV.
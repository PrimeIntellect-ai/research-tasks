You are a data analyst working with a dataset of network interactions. Your goal is to write a Bash script that performs lightweight graph analytics and pattern matching on a CSV file using standard CLI tools like `sqlite3` and `jq`.

You have been provided with a CSV file at `/home/user/network.csv` which contains an edge list representing a directed graph. The file has a header: `source,target`.

Write a Bash script at `/home/user/analyze.sh` that does the following:
1. Identifies the "most central" node in the graph based on degree centrality. For this task, a node's degree is the sum of its unique out-edges (where it is the source) and unique in-edges (where it is the target). If there is a tie, select the node that comes first alphabetically.
2. For this central node, perform a knowledge graph pattern match to find all of its "Friend-of-a-Friend" (FOAF) nodes. A FOAF is defined as any node `Z` where there is a directed path `Central -> Y -> Z`, subject to the constraints that:
   - There is NO direct edge `Central -> Z`.
   - `Z` is not the central node itself (`Z != Central`).
3. Export the result to `/home/user/result.json` in the following exact JSON format (ensure the `foaf` array is sorted alphabetically):
   ```json
   {
     "central_node": "NodeName",
     "foaf": [
       "FOAF_Node1",
       "FOAF_Node2"
     ]
   }
   ```

Make sure your script `/home/user/analyze.sh` is executable and creates the target JSON file when run. You may create temporary files if needed, but the final output must be precisely at `/home/user/result.json`.
You are an AI assistant helping a bioinformatics researcher organize a protein-protein interaction dataset and build a graph querying tool.

The researcher has provided a raw edge list of protein interactions in a TSV file at `/home/user/network.tsv`. The file has three columns: `Source_Protein`, `Target_Protein`, and `Interaction_Type`.

However, not all interactions are currently considered valid for this study. The lab has provided a scanned note containing the current inclusion rules, located at `/app/rules.png`. You must read this image to determine which interaction types to include in your materialized graph.

Your objective is to:
1. Extract the filtering rules from `/app/rules.png`.
2. Materialize a filtered version of the graph that only includes the valid edges (the graph is undirected, meaning an edge from A to B also implies B to A).
3. Write a Bash script at `/home/user/query.sh` that takes two arguments: a `Source_Protein` and a `Target_Protein`. 
4. The script `/home/user/query.sh` must compute the unweighted shortest path length (number of hops) between the two proteins in the filtered, undirected graph. 

Requirements for `/home/user/query.sh`:
- It must be written entirely in Bash (standard coreutils like `awk`, `grep`, `sed`, `join` are allowed and encouraged).
- It must take exactly two arguments: `$1` (Start Node) and `$2` (End Node).
- It must output *only* the integer length of the shortest path to standard output. 
- If the start node is the same as the end node, the distance is 0.
- If there is no path between the two nodes, it should output `-1`.
- The script must be optimized enough to traverse a network of ~500 nodes and ~1000 edges quickly.

Your final deliverable is the executable script `/home/user/query.sh`. An automated fuzzer will test your script against a hidden oracle by feeding it hundreds of random protein pairs to ensure your graph traversal and filtering logic are completely accurate.
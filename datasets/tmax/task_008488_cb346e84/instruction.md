You are a mobile build engineer maintaining an internal pipeline. We have a set of core modules that have developed circular dependencies, which breaks our traditional topological sort build order. 

To determine which module to treat as the "root" for our incremental build cache, we need to rank them using a custom PageRank-like weighting algorithm. You are provided with the dependency graph in JSON format at `/home/user/deps.json`.

Write a Bash script at `/home/user/calculate.sh` that reads `/home/user/deps.json` and calculates the build weight for each node over exactly 3 iterations.

The algorithm rules are:
1. At Iteration 0, the weight `W_0(N)` of every node is exactly 100.
2. For Iteration `i` from 1 to 3, the new weight is calculated as:
   `W_i(N) = 100 + SUM( W_{i-1}(M) / OutDegree(M) )` for all nodes `M` that have an edge directed to `N` (`M -> N`).
3. Use integer division (truncating towards zero) for each `W_{i-1}(M) / OutDegree(M)` term *before* adding it to the sum.
4. Nodes with an OutDegree of 0 do not distribute their weight.

Your bash script must serialize the final weights (Iteration 3) into a valid JSON file at `/home/user/weights.json` where the keys are the node IDs (as strings) and the values are the computed integer weights.
Example format: `{"10": 150, "20": 225}`

After computing the weights, identify the node ID with the highest weight at Iteration 3. If there is a tie, select the lowest node ID. 

Using x86_64 assembly, write a minimal standalone Linux program at `/home/user/artifact.s` that immediately exits with an exit status code equal to the winning node ID. Assemble and link this program using `nasm` and `ld` to produce a working executable at `/home/user/artifact`.

Ensure that `nasm` is installed on your system if you need it.
You are a bioinformatics analyst working on a new sequence analysis pipeline. Your task is to build a Rust application that processes DNA reads, constructs an overlap graph, identifies a target sequence, and calculates a statistical primer score using a numerically stable function.

Create a new Rust project named `bio_graph` in `/home/user/`.
Your application must do the following:

1. **Read input:** Parse the file `/home/user/reads.txt`. Each line contains a single DNA sequence.
2. **Parallel Overlap Graph (Graph Algorithms & Parallel Computing):** 
   - Use the `rayon` crate to parallelize the overlap detection.
   - Use the `petgraph` crate to build a directed graph where each node represents a sequence (using its line index, 0-indexed).
   - An directed edge exists from node A to node B if the exact suffix of length 7 of sequence A matches the exact prefix of length 7 of sequence B. (Do not add self-edges).
3. **Component Analysis:** Find the largest weakly connected component in this graph. Record the number of nodes in this largest component.
4. **Target Identification (Primer Design):** Within that largest component, find the node with the highest out-degree. If there is a tie, pick the one with the lowest node index. The "primer" is the first 20 characters of this sequence.
5. **Thermodynamic Score (Numerical Stability):** 
   - The statistical thermodynamic penalty for the primer is modeled by the function $f(x) = \frac{1 - \cos(x)}{x^2}$.
   - You must evaluate this penalty for $x = 10^{-8}$ as an `f64`. 
   - *Note:* A naive implementation of this formula in floating-point arithmetic suffers from catastrophic cancellation near $x=0$. You must write a numerically stable version of this evaluation to get the correct non-zero score.
6. **Output:** Produce a JSON file at `/home/user/result.json` with exactly this structure:
   ```json
   {
     "largest_component_size": 10,
     "target_primer": "ATGC...",
     "stability_score": 0.5000
   }
   ```
   (Make sure the `stability_score` is accurate to at least 4 decimal places).

Compile your application in release mode and run it to produce the output file.
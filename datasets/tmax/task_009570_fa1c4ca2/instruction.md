You are a machine learning engineer preparing training data for a Graph Neural Network (GNN). You are extracting a "Total Graph Energy" feature from molecular networks, which is defined as the sum of all edge weights in a graph.

Previously, your pipeline yielded non-reproducible features across runs because floating-point weights were summed in an arbitrary order (due to upstream parallel edge generation). In floating-point arithmetic, $ (A + B) + C \neq A + (B + C) $. To guarantee reproducibility, the reduction order must be strictly deterministic.

You have a directory of molecular graphs located at `/home/user/graphs/`. Each file is named `graph_<id>.txt` and contains an edge list where each line represents an edge:
`NodeA NodeB Weight` (space-separated, `Weight` is a floating-point number).

Your task is to:
1. Write a Bash script at `/home/user/calc_energy.sh` that computes the reproducible Total Graph Energy for every `.txt` file in `/home/user/graphs/`.
2. To ensure strict floating-point reproducibility, your script must extract the weights (3rd column), sort them in strictly ascending numerical order, and then sum them sequentially. Use `awk '{sum += $1} END {printf "%.10f\n", sum}'` for the accumulation to standardize the output format.
3. Your script must output these features to `/home/user/features.txt`. Each line should be formatted exactly as `filename: sum` (e.g., `graph_1: 4.1234500000`). The lines in `features.txt` must be sorted alphabetically by filename.
4. One of the graphs, `graph_0.txt`, is a perfectly regular star graph used for analytical validation. Its 20 edge weights form a geometric sequence: $1/2^1, 1/2^2, ..., 1/2^{20}$. The analytical sum of this infinite series approaches 1, but for 20 terms, the exact mathematical sum is $1 - 2^{-20}$. Calculate the absolute difference between your pipeline's computed energy for `graph_0` and the exact analytical value (using at least 10 decimal places of precision). Write this single absolute difference value to `/home/user/validation.txt`.

Ensure your bash script is executable and run it to generate `/home/user/features.txt` before completing the task.
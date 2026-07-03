You are a performance engineer tasked with optimizing a slow bioinformatics pipeline that analyzes spatial transcriptomics meshes. The pipeline maps molecular sequence differences across a physical mesh grid. 

Currently, the analysis is done manually using an inefficient combination of spreadsheets and slow tools. Your goal is to automate the bottleneck step by writing a fast, executable script.

You have been provided two files:
1. `/home/user/mesh_graph.tsv`: A tab-separated file representing edges in the spatial mesh. Each line contains: `Node1 Node2 Weight`
2. `/home/user/primers.tsv`: A tab-separated file containing the designed DNA primer sequence for each node. Each line contains: `NodeID Sequence` (all sequences are exactly 10 characters long, containing only A, C, G, T).

Write an executable script at `/home/user/run_analysis.sh` (you can use bash, awk, python, etc., but it must be runnable as `./run_analysis.sh mesh_graph.tsv primers.tsv`).

The script must:
1. Read the two provided files.
2. Identify the single edge in the mesh graph with the maximum integer weight. (Assume there is a unique maximum).
3. Retrieve the primer sequences for the two nodes connected by this maximum-weight edge.
4. Calculate the Hamming distance between these two sequences (the number of positional differences between the two strings).
5. Print ONLY the integer Hamming distance to standard output.

Once you have created the script, run it on the provided files and redirect the output to `/home/user/metric.txt`.

Example execution:
`./run_analysis.sh /home/user/mesh_graph.tsv /home/user/primers.tsv > /home/user/metric.txt`
You are a performance engineer tasked with optimizing a bioinformatics data processing workflow. 

In `/home/user/pipeline`, there is a basic bash-based workflow orchestration script named `orchestrator.sh` that sequentially executes three steps on a dataset of DNA sequences (`/home/user/pipeline/sequences.txt`):
1. `step1_primer_extract.sh`: Extracts potential primer motifs.
2. `step2_alignment_filter.sh`: Filters sequences based on simple alignment rules.
3. `step3_graph_build.sh`: Constructs a molecular overlap graph (adjacency list) where edges are formed if the 4-base suffix of one sequence matches the 4-base prefix of another.

Currently, the pipeline takes too long to execute due to a severe performance bottleneck in one of the steps. 

Your tasks are:
1. **Profile the workflow:** Identify which of the three step scripts is the bottleneck. Write the exact filename of the slowest script (e.g., `step1_primer_extract.sh`) into `/home/user/slowest_step.txt`.
2. **Optimize the bottleneck:** Rewrite the slow bash script to be highly efficient using standard Linux text processing tools (like `awk`, `sed`, `grep`, or optimized bash built-ins). The optimized script must produce the *exact same* output format as the original, but the entire `orchestrator.sh` must finish in under 1 second. 
3. **Execute the pipeline:** Run `./orchestrator.sh` so that it completely processes `/home/user/pipeline/sequences.txt` and generates the final output file `/home/user/pipeline/graph_output.txt`.

Ensure your rewritten script correctly handles the logic and outputs the graph edges in the format `SEQUENCE1 -> SEQUENCE2` for all valid overlaps, excluding self-edges (a sequence overlapping with itself).
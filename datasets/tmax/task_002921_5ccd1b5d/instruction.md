I am a researcher organizing a large dataset of scientific citations, which forms a complex directed graph of dependencies. Years ago, a former colleague wrote a high-performance tool in C to calculate the "Impact Depth" of a given paper. The Impact Depth is calculated recursively based on the citation tree.

Unfortunately, we lost the source code, and I only have a compiled, stripped Linux binary located at `/app/impact_calculator`. We need to integrate this logic into a modern pipeline that runs strictly on Bash.

Your task is to write a Bash script `/home/user/impact.sh` that perfectly replicates the behavior of `/app/impact_calculator`.

The binary `/app/impact_calculator` takes a single file as an argument. The file contains a list of directed edges representing citations. Each line is formatted as `Paper_A -> Paper_B`, meaning Paper A cites Paper B. The first line of the file is always the target paper ID whose Impact Depth needs to be calculated, prefixed with `TARGET:`.

For example, an input file `/tmp/sample_graph.txt` might look like:
TARGET: P1
P1 -> P2
P1 -> P3
P2 -> P4
P3 -> P4

The binary outputs a single integer to standard output, representing the calculated Impact Depth. You can run `/app/impact_calculator /tmp/sample_graph.txt` to observe its behavior.

You must reverse-engineer the logic (which involves graph traversal, recursive depth counting, and specific aggregation rules for multiple paths) by probing `/app/impact_calculator` with various mock datasets.

Once you understand the algorithm, implement it in `/home/user/impact.sh`. Your script must take a single file path as an argument and print exactly the same integer output as the binary. Your script must be written purely in Bash, utilizing standard Linux utilities (like `awk`, `grep`, `sed`, `sort`, `bash` arrays/functions) to simulate the recursive graph queries and aggregation.

Ensure your script is executable (`chmod +x /home/user/impact.sh`). The automated verifier will test your script against the binary using hundreds of randomly generated graph files.
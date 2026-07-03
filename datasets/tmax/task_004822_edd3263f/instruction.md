You are assisting a researcher in tracing the lineage of datasets and research papers. 

The researcher has extracted a citation graph into a tab-separated values file located at `/home/user/citations.tsv`. Each line represents a directed edge in the citation graph: the first column is the ID of the citing paper, and the second column is the ID of the cited paper (e.g., `P001\tP002` means P001 cites P002).

Your task is to:
1. Compute the shortest citation path from paper `P001` to paper `P099`.
2. Export this path into a JSON file located at `/home/user/path.json`.

The output file `/home/user/path.json` must exactly match this format:
```json
{
  "path": ["P001", "PXXX", "PYYY", "P099"]
}
```

Constraints:
- You must solve this using ONLY Bash shell built-ins, `awk`, `sed`, `grep`, and standard GNU coreutils. 
- You are explicitly forbidden from using Python, Perl, Ruby, Node.js, or any other high-level scripting languages. 
- If there are multiple paths of the same shortest length, you may output any of them (though in this dataset, the shortest path is unique).
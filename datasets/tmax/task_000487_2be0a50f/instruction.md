You are an AI assistant helping a researcher organize their academic datasets. The researcher has data in multiple formats representing a knowledge graph of papers, authors, and citations. They are trying to identify anomalous "circular citations" (specifically, exact 3-cycles where Paper A cites Paper B, Paper B cites Paper C, and Paper C cites Paper A) which behave like a deadlock in their dependency resolution tool.

Your task is to write a pure Bash script at `/home/user/process_graph.sh` that processes these files, identifies the 3-cycles, maps them to the authors, and materializes the result into a specific JSONL format.

**Input Data:**
1. `/home/user/authors.jsonl` (Document format)
   Format: `{"author_id": "A1", "name": "Dr. Smith"}`
2. `/home/user/papers.csv` (Relational format)
   Format: `paper_id,title,author_id`
   (Note: Includes a header row. Each paper has exactly one author).
3. `/home/user/citations.txt` (Graph edge list format)
   Format: `P1 -> P2` (meaning P1 cites P2, separated by " -> ")

**Requirements for `/home/user/process_graph.sh`:**
1. The script must be pure Bash (using coreutils, `awk`, `sed`, `jq`, `join`, `sort`, etc.). Do not use Python, Perl, or Ruby.
2. Find all citation 3-cycles (A -> B -> C -> A). 
3. Map the papers in these cycles to their respective author names.
4. Materialize the projection into a new file: `/home/user/circular_citations.jsonl`.
5. The output must strictly follow this JSON schema for each cycle found (one JSON object per line):
   ```json
   {
     "cycle_id": "P1-P2-P3",
     "authors": ["AuthorName1", "AuthorName2", "AuthorName3"]
   }
   ```
   - `cycle_id` must be the three `paper_id`s in the cycle, joined by hyphens, **sorted lexicographically** (e.g., if the cycle involves P3, P1, and P5, the ID must be `P1-P3-P5` regardless of the citation direction).
   - `authors` must be an array of the names of the authors of the three papers, **sorted alphabetically**.
   - Ensure the JSON lines in the output file are also sorted alphabetically by `cycle_id` so the file is deterministic.

The script should have executable permissions and run without any arguments. Once you have written the script, execute it to generate the `/home/user/circular_citations.jsonl` file.
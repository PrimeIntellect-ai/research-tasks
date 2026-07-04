A researcher is organizing a dataset of academic papers and needs to project their citation network from a document-oriented representation into a graph-like metric. 

You have been provided with a Rust Cargo project located at `/home/user/citation_graph`. Inside this project, there is a dataset file at `/home/user/citation_graph/data/papers.jsonl`. 
Each line in this file is a JSON object representing a paper, with the following schema:
- `id` (string): The unique identifier of the paper.
- `title` (string): The title of the paper.
- `references` (array of strings): A list of `id`s of other papers that this paper cites.

Your task is to write a Rust program in `/home/user/citation_graph/src/main.rs` that reads this JSONL file, projects it into a directed graph (where edges represent citations from one paper to its references), and aggregates the in-degrees (number of citations received) for all referenced papers. 

The program must find the paper `id` that has the highest in-degree (most cited). Once identified, the program should write ONLY this winning paper `id` (as a plain string, no quotes or newlines) to `/home/user/top_cited.txt`. 

The Cargo project is already initialized with `serde` and `serde_json` dependencies. You should implement the logic, build, and run the project using `cargo run` to generate the final output file.
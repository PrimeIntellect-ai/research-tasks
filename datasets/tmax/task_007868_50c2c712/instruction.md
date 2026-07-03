You are an AI assistant helping a dataset researcher organize their data pipeline. 

The researcher has datasets in multiple formats (CSV and JSON) and wants to merge them into a single graph database. Before loading the data, they want to analyze it for "deadlocks" (circular citations) and generate a Cypher script to initialize the graph.

You must create a bash script at `/home/user/build_graph.sh` that processes the following three files located in `/home/user/datasets/`:

1. `researchers.csv`: A comma-separated file with headers `researcher_id,name,project_id`.
2. `projects.json`: A JSON array of objects. Each object has `project_id`, `title`, and `publications` (an array of publication IDs).
3. `citations.csv`: A comma-separated file with headers `citing_pub_id,cited_pub_id`. This represents an edge list of citations.

Your script must perform the following actions using standard Bash CLI tools (like `awk`, `jq`, `sort`, `join`, etc.):

**1. Detect Deadlocks (Circular Dependencies):**
Find all instances of bidirectional citations (i.e., PUB_A cites PUB_B AND PUB_B cites PUB_A). 
Output these pairs to `/home/user/deadlock_citations.log`. 
Each line must be formatted as `PUB_A<->PUB_B`, where the lexicographically smaller ID is always on the left. The lines in the log file should be sorted alphabetically.

**2. Aggregate Citation Counts:**
Calculate the total number of times each publication is cited by *other* publications in `citations.csv`.

**3. Generate Cypher Script:**
Your script must output a Cypher script to `/home/user/init.cypher` that maps this data into graph nodes and relationships. The generated Cypher script must contain exactly the following formatted statements, sorted alphabetically by the statement string:

* For each publication: `CREATE (:Publication {id: '<pub_id>', citation_count: <count>});`
* For each researcher: `CREATE (:Researcher {id: '<researcher_id>', name: '<name>'});`
* For each project: `CREATE (:Project {id: '<project_id>', title: '<title>'});`
* For researcher-project relations: `CREATE (<researcher_id>)-[:WORKS_ON]->(<project_id>);`
* For project-publication relations: `CREATE (<project_id>)-[:PRODUCED]->(<pub_id>);`
* For citations: `CREATE (<citing_pub_id>)-[:CITES]->(<cited_pub_id>);`

*(Note: In the relationship generation, just use the raw IDs as text in the cypher statement like `CREATE (R1)-[:WORKS_ON]->(P1);` for the sake of this textual export, do not worry about Cypher variable bindings).*

Ensure your script is executable (`chmod +x /home/user/build_graph.sh`) and run it so the output files are generated.
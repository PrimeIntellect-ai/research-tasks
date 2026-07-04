You are assisting a researcher in organizing a complex dataset of academic paper citations. The researcher has provided a Cypher script containing the citation graph data, but needs a reliable way to query it programmatically.

Your task is to:
1. Start a local graph database using Docker. Specifically, run a `neo4j:5` container named `research_graph` in the background, exposing the standard HTTP port (7474) and Bolt port (7687) to the host. Disable authentication by setting the environment variable `NEO4J_AUTH=none`.
2. Wait for the database to become fully ready.
3. Load the graph data into the database from the file `/home/user/graph_setup.cypher`. (You will need to use `cypher-shell` inside the container or the HTTP API to execute it).
4. Write a Bash script at `/home/user/get_dependencies.sh` that takes exactly one argument: a Paper ID (e.g., "P1").
5. The Bash script must use `curl` to send a **parameterized query** to the Neo4j HTTP API (`http://localhost:7474/db/neo4j/tx/commit`). 
6. The Cypher query in your script must be a recursive/hierarchical query that finds all distinct `Paper` nodes that the provided Paper ID cites, directly or indirectly, up to a maximum depth of 3 hops (using the `CITES` relationship).
7. The script must parse the JSON response (using `jq` or similar tools), extract the IDs of the cited papers, sort them alphabetically, and write them to `/home/user/output.txt`, with one paper ID per line.

Ensure that `/home/user/get_dependencies.sh` is executable. You should test your script by running `/home/user/get_dependencies.sh P1` to ensure it successfully generates `/home/user/output.txt` with the correct format.
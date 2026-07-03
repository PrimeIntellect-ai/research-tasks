You are a database administrator tasked with optimizing a graph database query. 

We are querying an infrastructure knowledge graph stored in an RDF format (`/home/user/infra.ttl`). We have a Bash script (`/home/user/bad_query.sh`) that uses `roqet` (a command-line SPARQL query utility) to find all employees who have access to servers running software with a specific vulnerability.

However, the current SPARQL query inside the script has a critical flaw: it is missing a relationship link in the graph pattern matching. This missing constraint acts like an implicit cross join, causing a Cartesian product. It incorrectly pairs every employee in the database with every vulnerable server, regardless of whether the employee actually has access to that server.

Your tasks are:
1. Install the `rasqal-utils` package (which provides the `roqet` command) using the system package manager.
2. Analyze `/home/user/infra.ttl` and `/home/user/bad_query.sh`.
3. Create a new script at `/home/user/optimized_query.sh` that fixes the query. 
4. The new script must:
   - Accept the vulnerability ID (e.g., "CVE-2023-1234") as the first Bash positional parameter (`$1`) and dynamically parameterize it in the SPARQL query.
   - Fix the graph pattern matching so it only returns employees who *actually access* the specific vulnerable servers.
   - Select two variables: `?employeeName` and `?server`.
   - Sort the results alphabetically by `?employeeName` in ascending order.
   - Paginate the results to return a maximum of 2 records (using SPARQL LIMIT).
   - Execute `roqet` returning standard JSON format (`-r json`).
5. Run your script with the argument `CVE-2023-1234` and save the exact JSON output to `/home/user/results.json`.

Ensure your script is executable. Do not modify the original `.ttl` file.
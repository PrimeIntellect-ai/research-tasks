You are a database administrator managing an enterprise cybersecurity knowledge graph. We recently discovered a critical logic flaw in our asset compliance reporting. Our legacy reporting script was using direct string concatenation to build SPARQL queries (which is inefficient and a security risk) and had a "stale data" bug: it considered a server "safe" from a vulnerability if *any* patch for it was installed, failing to check if the patch status was 'Superseded' or 'Revoked' (essentially reading stale patch indexes).

Your task is to write a new Python script that queries our local RDF knowledge graph and accurately reports vulnerable servers. 

Here are the details:
1. The knowledge graph is located at `/home/user/security_graph.ttl` (in Turtle format). 
2. The schema uses the following custom namespaces:
   - Prefix `ex:` -> `http://example.org/sec#`
   - Relationships: `ex:hasVuln` (Server to CVE), `ex:hasPatch` (Server to Patch), `ex:fixes` (Patch to CVE), `ex:status` (Patch to String).
   - Entities: Servers have names like `ex:Server_1`.
3. Write a Python script at `/home/user/audit_vulnerabilities.py`. 
4. The script must use the `rdflib` library (you may need to install it).
5. The script must define a parameterized SPARQL query. It should take a specific CVE ID (e.g., `ex:CVE-2023-9999`) as a bound parameter (using `initBindings` or prepared queries, do NOT use Python string formatting/concatenation to insert the CVE).
6. The SPARQL query must match the following knowledge graph pattern: Find all servers that have the target vulnerability, BUT filter out servers that have an `ex:hasPatch` relationship to a patch that `ex:fixes` the target vulnerability AND has an `ex:status` of exactly `"Active"`. (If a server only has "Superseded" patches for the CVE, it is still vulnerable).
7. Execute the script targeting `http://example.org/sec#CVE-2024-1111` as the parameter.
8. The script must write the plain text hostnames (the URI fragment, e.g., `Server_A`) of the vulnerable servers, one per line, sorted alphabetically, into `/home/user/vulnerable_servers.log`.

Do not use brute-force Python iteration to solve the graph matching; the filtering must be done within the SPARQL query itself using graph query languages and pattern matching features (like `MINUS` or `FILTER NOT EXISTS`).
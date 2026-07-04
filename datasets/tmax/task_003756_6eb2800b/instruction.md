You are acting as a compliance officer auditing an enterprise data system. We need to detect queries that attempt to bypass our access controls or perform unauthorized bulk data exfiltration. 

The system uses a mix of relational data (users), document stores (resource metadata), and a graph database (access paths). You are provided with a proprietary, stripped query analyzer binary at `/app/query_analyzer`. This binary evaluates cross-representation queries and outputs a serialized execution plan and index strategy.

Your objective is to build a Bash script `/home/user/detector.sh` that acts as a query sanitizer.
It must read a single query definition file (JSON format, containing parameterized queries and graph analytics instructions) and decide whether it is a legitimate ("clean") query or a compliance violation ("evil").

Requirements for `/home/user/detector.sh`:
1. It must accept exactly one argument: the path to the query definition file.
2. It should exit with code `0` if the query is clean (allowed).
3. It should exit with code `1` if the query is evil (rejected/flagged).
4. You may use `/app/query_analyzer` to help analyze the query. You will need to reverse-engineer its usage or treat it as a black box to understand how it exposes query plans, index bypasses, or unauthorized graph centrality computations.

To aid your development, we have provided sample corpora:
- `/home/user/samples/evil/`: Contains known malicious queries that force full-scans on sensitive documents or misuse graph analytics for reconnaissance.
- `/home/user/samples/clean/`: Contains normal operational queries.

Your final `detector.sh` will be tested against a hidden test corpus of clean and evil queries. You must achieve a 100% success rate on the hidden corpus. Ensure your script is robust and correctly handles parameterized query structures.
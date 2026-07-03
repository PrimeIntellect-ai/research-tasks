You are assisting a compliance officer in auditing system access logs. 

We have a Python script located at `/home/user/generate_report.py` that is supposed to generate an access audit report. Currently, the script reads an SQLite database (`/home/user/audit_logs.db`) to count how many times each department accessed the 'FIN-01' system. However, the compliance officer noticed the numbers are massively inflated due to a bad SQL query in the script (an implicit cross join).

Additionally, the compliance requirements have changed. Instead of hardcoding 'FIN-01', the report must dynamically identify all systems classified as "HighRisk" by querying our IT infrastructure knowledge graph, which is stored as an RDF Turtle file at `/home/user/system_graph.ttl`.

Your task is to:
1. Fix the SQL query in `/home/user/generate_report.py` so it properly joins the `employees` and `access_events` tables.
2. Update the script to parse `/home/user/system_graph.ttl` using the `rdflib` library and run a SPARQL query to find all systems that are of type `http://example.org/ontology#HighRiskSystem`.
3. For every high-risk system identified, query the corrected SQLite database to get the true count of access events per department for that system.
4. Export the final results to `/home/user/compliance_report.csv`.

The output CSV must have exactly these three columns: `department,system_name,access_count`.
The CSV must include headers, and the rows must be sorted alphabetically by `department`, and then by `system_name`. Ensure you only list combinations that have an `access_count` greater than 0.

You may install `rdflib` if it is not already installed (`pip install rdflib`).
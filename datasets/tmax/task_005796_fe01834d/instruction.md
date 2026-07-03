You are acting as an automated assistant for a compliance officer auditing corporate systems. We suspect there are undetected conflicts of interest where employees have administrative access to internal systems while simultaneously consulting for third-party vendors that service those exact systems.

We have exported our corporate access and vendor management records into an RDF Knowledge Graph (Turtle format) located at `/home/user/audit_data.ttl`.

Your task is to write a Python script (`/home/user/find_conflicts.py`) that uses SPARQL to query this knowledge graph and identify these conflicts.

Specifically, the script must find all instances where:
1. An `Employee` has admin access to a `System` (using the predicate `http://example.org/audit#hasAdminAccess`).
2. That same `Employee` consults for a `Vendor` (using the predicate `http://example.org/audit#consultsFor`).
3. That same `Vendor` provides services to that same `System` (using the predicate `http://example.org/audit#providesServiceTo`).

Requirements:
- You may use the `rdflib` Python package. Install it via `pip install rdflib` if it is not present.
- The script must execute a SPARQL query to perform the pattern matching.
- The output must be written to a CSV file at `/home/user/conflict_report.csv`.
- The CSV file must contain exactly three columns: `employee_uri`, `vendor_uri`, and `system_uri`.
- The CSV must NOT have a header row.
- The results must be sorted in **descending alphabetical order** based on the `employee_uri`.
- Ensure your script runs and successfully generates the output file.
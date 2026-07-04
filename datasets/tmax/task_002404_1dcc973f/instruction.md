You are a compliance officer auditing an organization's IT infrastructure. The system's architecture is modeled as a Knowledge Graph. Your goal is to build an automated auditing pipeline in C that detects specific security compliance violations: specifically, any `PublicFacing` system that connects to a `PIIDatabase` through an unencrypted `API`.

You have been provided with the system infrastructure graph in Turtle format. 

First, create the file `/home/user/system_graph.ttl` with the following exact contents:
```turtle
@prefix sys: <http://example.org/sys#> .

sys:AppServer1 a sys:PublicFacing ;
    sys:connectsTo sys:InternalAPI_A .
sys:InternalAPI_A a sys:API ;
    sys:hasEncryption "false" ;
    sys:connectsTo sys:UserDB .
sys:UserDB a sys:PIIDatabase .

sys:AppServer2 a sys:PublicFacing ;
    sys:connectsTo sys:InternalAPI_B .
sys:InternalAPI_B a sys:API ;
    sys:hasEncryption "true" ;
    sys:connectsTo sys:UserDB .

sys:AdminPortal a sys:InternalSystem ;
    sys:connectsTo sys:InternalAPI_C .
sys:InternalAPI_C a sys:API ;
    sys:hasEncryption "false" ;
    sys:connectsTo sys:HRDB .
sys:HRDB a sys:PIIDatabase .

sys:WebFront a sys:PublicFacing ;
    sys:connectsTo sys:InternalAPI_D .
sys:InternalAPI_D a sys:API ;
    sys:hasEncryption "false" ;
    sys:connectsTo sys:FinancialDB .
sys:FinancialDB a sys:PIIDatabase .
```

Your task is to build a C-based pipeline to find the violations. 

Perform the following steps:
1. Create a Python virtual environment at `/home/user/venv` and install the `rdflib` package, which provides a standard SPARQL evaluation engine.
2. Write a short Python script at `/home/user/query_runner.py` that reads a SPARQL query file (passed as the first argument) and a Turtle file (passed as the second argument), executes the query using `rdflib`, and prints the raw result rows as space-separated values (just the node names, not the full URIs).
3. Write a C program at `/home/user/auditor.c`. This program must:
   - Construct a valid SPARQL query to find all instances where a `sys:PublicFacing` entity connects to a `sys:API` with `sys:hasEncryption "false"`, which in turn connects to a `sys:PIIDatabase`.
   - Select the names of the public server, the API, and the database in that order.
   - Write this SPARQL query to a temporary file `/home/user/query.rq`.
   - Use `popen()` or similar standard C process-chaining mechanisms to execute your Python script (`/home/user/venv/bin/python /home/user/query_runner.py /home/user/query.rq /home/user/system_graph.ttl`).
   - Read the standard output from the Python script.
   - For each violation found, append a line to `/home/user/audit_violations.log` in the exact format: `VIOLATION: [Public Node] connects to [API Node] connects to [DB Node]` (e.g., `VIOLATION: AppServer1 connects to InternalAPI_A connects to UserDB`).
4. Compile your C program to `/home/user/auditor` and run it.

Ensure your C program robustly handles the pipeline chaining and correctly parses the output from the graph pattern matching step. Sort the final output in `/home/user/audit_violations.log` alphabetically by the Public Node name if there are multiple violations.
You are acting as a Database Administrator tasked with analyzing and optimizing queries for a microservices dependency tracker. 

We have a local SQLite database at `/home/user/architecture.db` that represents a knowledge graph of our internal microservices. The database contains two tables that model the nodes and edges of our service architecture. You need to inspect the database schema to understand how services and their dependencies (callers and callees) are stored.

Currently, developers are manually tracing service outages using inefficient, string-concatenated queries that are vulnerable to SQL injection. Your task is to write a secure, optimized Python script that performs graph pattern matching to determine the "blast radius" of a service outage.

Write a Python script at `/home/user/analyze_impact.py` that meets the following requirements:
1. It takes exactly one command-line argument: the name of a target service (e.g., `python3 /home/user/analyze_impact.py "PaymentGateway"`).
2. It must query the local SQLite database using **strictly parameterized queries** (no string formatting for the service name) to prevent SQL injection.
3. It must find all upstream services that are impacted if the target service goes down. An upstream service is considered impacted if:
   - It directly calls the target service, AND the dependency is marked as critical.
   - OR, it directly calls an impacted service from the step above, AND the dependency is marked as critical.
   (In other words, find all critical upstream dependencies at depth 1 and depth 2).
4. The script must output the final list of impacted service names into a JSON file at `/home/user/impact.json`. The output must exactly match this format:
   ```json
   {
       "target": "TargetServiceName",
       "impacted": ["ImpactedServiceA", "ImpactedServiceB"]
   }
   ```
   The `impacted` list must be sorted alphabetically and should not contain duplicates or the target service itself.

Once your script is ready, execute it for the target service `"PaymentGateway"` so that `/home/user/impact.json` is generated.
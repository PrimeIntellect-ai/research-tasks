You are a data scientist troubleshooting a non-reproducible graph analysis pipeline. We have a microservice that computes a specific structural metric from simplified PDB data, but floating-point accumulation errors are causing discrepancies across different machines. 

Your task is to implement a numerically stable version of the metric calculator and integrate it into our service mesh.

Part 1: Numerically Stable Implementation
Write a script at `/home/user/graph_metric.py` that reads a simplified PDB format from standard input.
The input consists of multiple lines like:
`ATOM <id> <x> <y> <z>`
where x, y, and z are standard floating-point coordinates. Ignore any malformed lines or lines not starting with `ATOM`.

For this set of atoms:
1. Build a neighbor graph where an edge exists between two atoms if their Euclidean distance is strictly less than 1.0.
2. For each atom, determine its degree (number of connected neighbors).
3. We need to compute a global metric: the sum of `1.0 / (degree + 1.0)` for all valid atoms.
4. Numerical Stability Rule: To ensure bit-exact reproducibility and eliminate floating-point reduction order issues, compute the metric term for each atom as a 64-bit float. Then, sort these terms in strictly ascending numerical order. Finally, sum them sequentially from smallest to largest using standard floating-point addition.
5. Print the final sum to standard output, formatted to exactly 8 decimal places (e.g., `4.50000000`).

Ensure your script is executable and relies only on standard Python 3 libraries.

Part 2: Service Composition
We have a multi-service environment that needs to be stitched together:
1. A Flask application is located at `/app/api.py`. It is currently incomplete. Modify it so that it listens on port 5000. It must expose a `POST` endpoint at `/calc`. When this endpoint receives a raw text payload (the PDB data), it should invoke your `/home/user/graph_metric.py` script via a subprocess, passing the payload via stdin, and return the exact text output of the script with HTTP status 200.
2. Configure the system's Nginx server to listen on port 8080. It should proxy any requests starting with `/api/` to the Flask app. Specifically, a request to `http://localhost:8080/api/calc` must be correctly routed to the Flask app's `/calc` endpoint.
3. Start both the Flask app (as a background process) and Nginx.

Ensure everything is running and correctly bound to the specified ports when you finish. Automated tests will fuzz your `graph_metric.py` script against a hidden oracle using random PDB strings to verify bit-exact numerical stability, and will perform end-to-end HTTP tests through the Nginx gateway.
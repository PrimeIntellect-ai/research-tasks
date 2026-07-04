You are an AI assistant helping a compliance officer audit physical access to a highly restricted data center. 

We have collected security camera footage of the badge scanner and an export of our organizational knowledge graph. Your task is to identify employees who entered the room without proper authorization and expose this list via a web service for our automated compliance dashboard.

**Resources provided:**
1. `/app/entry_log.mp4`: A security camera video of the badge scanner. Every time an employee badges in, a QR code flashes on the scanner's screen containing their Employee ID (e.g., "EMP001"). 
2. `/app/org_graph.ttl`: An RDF knowledge graph in Turtle format detailing the corporate hierarchy. It uses the namespace `http://example.org/org#` (prefix `org:`). Relevant predicates include `org:reportsTo` and `org:hasRole`.

**Access Rules:**
An employee is authorized to enter the secure data center ONLY IF:
- They explicitly possess the role `org:Admin` (i.e., `<employee_uri> org:hasRole org:Admin`), OR
- They transitively report to someone (at any depth in the management chain) who possesses the `org:Admin` role. 
*Note: Any employee who does not meet this criteria is considered unauthorized.*

**Your Objective:**
1. Extract all unique Employee IDs from the QR codes in `/app/entry_log.mp4`. (Tools like `ffmpeg`, `opencv-python`, and `pyzbar` are pre-installed in your environment).
2. Query the knowledge graph (`/app/org_graph.ttl`) using SPARQL (e.g., via Python's `rdflib` and property paths) or recursive graph traversal to determine the authorization status of each extracted Employee ID.
3. Start an HTTP web server listening on `0.0.0.0:9090`.
4. Expose a `GET /unauthorized` endpoint. When requested, it must return a JSON response containing a flat array of strings representing the Employee IDs of all **unauthorized** individuals who badged in. The array must be sorted alphabetically. (Example: `["EMP012", "EMP099"]`).

Leave the server running in the foreground or background so the compliance dashboard can query it.
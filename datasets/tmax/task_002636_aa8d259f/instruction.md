You are a Database Reliability Engineer responding to a critical incident. Our automated backup integrity checker found a corrupted snapshot and left an automated audio report at `/app/incident_report.wav`. 

Our backup infrastructure consists of a chain of incremental snapshots. The dependency topology is stored as an RDF Turtle file at `/app/backup_topology.ttl`. The graph uses the prefix `http://example.org/backup/` and the predicate `http://example.org/backup/dependsOn` to indicate that a snapshot depends on a parent snapshot. If a parent is corrupted, all snapshots that transitively depend on it are also corrupted.

Your task is to build an impact analysis service:
1. Transcribe the audio file `/app/incident_report.wav` to discover the exact ID of the corrupted snapshot mentioned.
2. Build an HTTP API service (using Python, Node.js, or any language you prefer) that listens on `127.0.0.1:8080`.
3. Expose an endpoint `GET /api/impact` that accepts a query parameter `corrupted_id`.
4. The endpoint must execute a parameterized SPARQL query against the provided RDF graph to compute the transitive closure of all snapshots that depend on the given `corrupted_id`. 
5. Return the result as a JSON response in this exact format:
   `{"impacted": ["snapshot-a", "snapshot-b", ...]}`
   (The array should contain only the local name strings of the URIs, e.g., `snapshot-a`, not the full `http://example.org/backup/snapshot-a` URIs).
6. The service must handle chains of any length using SPARQL property paths.

Start the service and leave it running in the background. Do not hardcode the audio transcription into the graph logic; the endpoint must dynamically process the parameterized SPARQL query based on the `corrupted_id` parameter provided by the incoming HTTP request.
You are a Database Reliability Engineer managing backup systems. We store our backup metadata as an RDF graph.

We have a custom backup monitoring API service, pre-vendored at `/app/backup_graph_server`. This service exposes an HTTP endpoint to query failed backups for a specific date. However, the service is currently broken:
1. The package has a deliberate perturbation: the `start.sh` script contains a typo that prevents the service from launching.
2. The SPARQL query used to fetch failed backups (located in `/app/backup_graph_server/queries.py`) contains a logical flaw. Due to an implicit cross join (missing link between the Server and the BackupJob), it returns a Cartesian product of all servers and all failed jobs, instead of only the servers that actually own the failed jobs. 

Your tasks are to:
1. Identify and fix the perturbation in `/app/backup_graph_server/start.sh` so the service can start.
2. Correct the SPARQL query in `/app/backup_graph_server/queries.py` so it properly joins the `Server` and the `BackupJob` using the `<http://backup.local/vocab#hasJob>` predicate. The query should only return the `serverName` and `jobId` of jobs that actually belong to the server and have a status of "FAILED" for the requested date.
3. Start the service. It must listen on `0.0.0.0:9000`. Keep the service running in the background.

The RDF dataset is located at `/home/user/backups.ttl`. The API uses `rdflib` and Flask.
The endpoint to test is `GET /api/failed_backups?date=YYYY-MM-DD`. It must return a JSON array of objects, e.g., `[{"serverName": "db-server-1", "jobId": "job-101"}]`.
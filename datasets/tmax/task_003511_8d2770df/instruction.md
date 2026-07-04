You are a database reliability engineer managing a distributed backup metadata system. Our backup metadata is modeled as a knowledge graph, where nodes are backups, database instances, and storage zones, and edges are relationships like "derived_from" (for incremental backups) and "stored_in". 

We have a multi-service architecture running locally:
1. A PostgreSQL database (port 5432) storing the historical backup metadata.
2. A Redis instance (port 6379) used for caching backup validation states.
3. A local Nginx reverse proxy (port 8080) that routes backup registration requests.

Your task is to implement a C++ backup sanitization filter and configure the services to work together to validate incoming backup registrations.

First, you need to configure the services. There is a startup script at `/app/start_services.sh` which launches Postgres, Redis, and Nginx. You must configure Nginx (`/app/nginx/nginx.conf`) to proxy requests from `http://127.0.0.1:8080/register` to a local fastcgi or custom HTTP C++ service you will create on port `9000`.

Second, write a C++ program at `/home/user/backup_sanitizer.cpp` and compile it to `/home/user/backup_sanitizer`. This program will act as a CLI/HTTP hybrid. We will test it strictly as a CLI against two corpora of backup metadata JSON files located at `/app/corpora/clean/` and `/app/corpora/evil/`. 

Your C++ program must read a JSON file path as its first argument, process the backup knowledge graph, and exit with code `0` (accept) or code `1` (reject). 

To accept a backup graph (clean):
1. **Graph Traversal:** The shortest path from any incremental backup node to a "full" backup node via `derived_from` edges must be exactly 3 hops or fewer. 
2. **Pattern Matching:** No backup node may be `stored_in` a storage zone marked with `"status": "compromised"`.
3. **Analytical Aggregation:** The sum of `bytes` for any sliding window of the last 3 backups in the graph (sorted by `timestamp`) must not exceed 500GB (500000000000 bytes).

If any of these conditions are violated, or if the graph contains cyclic `derived_from` dependencies, the program must reject the JSON (exit code 1).

You must ensure that running `/home/user/backup_sanitizer <file.json>` correctly classifies 100% of the files in `/app/corpora/clean/` (exit 0) and rejects 100% of the files in `/app/corpora/evil/` (exit 1). Finally, configure your service to run on port 9000, read the same JSON payload from HTTP POST requests, and log accepted backup IDs to Redis (using a Redis list key named `valid_backups`).
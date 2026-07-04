You are a database reliability engineer stepping in to manage a recent backup corruption incident. 

We maintain a microservice dependency graph in an SQLite database located at `/app/microservices.db`. However, a recent incident caused an index to become corrupted, leading to stale rows being returned during backup operations and regular queries. 

An automated incident management system left an audio voicemail detailing the corruption. You can find this voicemail at `/app/incident_voicemail.wav`. 

Your objectives are to:
1. Transcribe the audio file to identify the name of the corrupted index.
2. Bypass or drop the corrupted index in your queries so you can retrieve the actual, uncorrupted base table data representing our microservice graph. The database contains two tables:
   - `services(id INTEGER PRIMARY KEY, name TEXT)`
   - `dependencies(source INTEGER, target INTEGER, latency INTEGER)`
3. Map this relational data into a graph representation in Python.
4. Write a parameterized Python CLI tool at `/home/user/query_path.py` that calculates the minimum latency path between any two services.

The script `/home/user/query_path.py` must take exactly two command-line arguments (source service `id`, target service `id`) and print ONLY the integer value of the shortest path (sum of latencies) between them to standard output. If no path exists, it must print `-1`.

Example usage:
`python3 /home/user/query_path.py 12 45`

The script must be highly reliable. An automated integration test will fuzz your script with hundreds of random pairs of service IDs to ensure it behaves exactly equivalently to our baseline oracle over the uncorrupted data.
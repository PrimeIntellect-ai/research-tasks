You are a data analyst investigating server performance anomalies. You have been given a dataset of server resource utilization in `/home/user/servers.csv`. The file has a header and four columns: `host`, `cpu`, `mem`, and `disk` (all metrics are percentages 0-100).

Your objective is to find the server that is most similar to a specific "profile" of interest, relying entirely on standard Linux command-line tools (like `awk`, `sort`, `head`, etc.). 

The target profile for the anomaly is:
- CPU: 85.0
- Memory: 20.0
- Disk: 60.0

Similarity should be determined by calculating the squared Euclidean distance between a server's metrics and the target profile. The server with the smallest squared Euclidean distance is the most similar.

Please perform this similarity search and save ONLY the hostname of the most similar server to the file `/home/user/similar_host.txt`. Do not include any trailing spaces or extra text in the file.
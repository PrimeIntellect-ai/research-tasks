You need to build a custom Kubernetes-like Python operator that manages reverse proxy routing based on real-time storage monitoring. 

We have three local mock "backend nodes" that receive file uploads. They store data in the following directories:
- `/home/user/data/node1`
- `/home/user/data/node2`
- `/home/user/data/node3`

Your tasks:
1. **Mock Backends:** Write a simple Python HTTP server and spawn three instances of it on ports 8081, 8082, and 8083. Any `POST /upload` request with a body should write a file to the respective node's directory and return a 200 OK.
2. **Reverse Proxy:** Configure a reverse proxy (e.g., Nginx or HAProxy) running as the current user on port 8080. It must load balance incoming HTTP requests across the three backend nodes. 
3. **Storage Operator:** Write a Python script `/home/user/operator.py`. This script must act as a continuous controller:
   - Monitor the disk usage (directory size) of each node's data directory.
   - The storage quota for each node is 50MB.
   - If a node's directory exceeds 80% of its quota (40MB), the operator must dynamically reconfigure the reverse proxy to stop sending new traffic to that node, and seamlessly reload the proxy configuration without dropping active connections.
   - You must simulate a simplified `fstab`-like tracking file at `/home/user/fstab_sim` that the operator reads on startup to know the directories, ports, and quotas. Create this file with a custom structured format.

**Testing & Verification:**
We have provided a stripped, proprietary binary at `/app/traffic_gen`. This binary acts as an adversarial load generator. It will continuously send upload requests to `http://127.0.0.1:8080/upload`. 
- It aggressively uploads files, which will cause the backends to fill up.
- If it detects a dropped connection (proxy restart failure) or if it manages to push a node's directory past the absolute 50MB limit (because your operator was too slow to evict it), it records a failure.
- Run `/app/traffic_gen --target http://127.0.0.1:8080`. It outputs a JSON summary upon completion.
- You must achieve a `success_rate` of at least 0.95 to pass the task.

Start the backends, the proxy, and your operator in the background, then ensure they are ready to handle the load generator.
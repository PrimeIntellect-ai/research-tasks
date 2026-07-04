You are a security researcher analyzing a suspicious data processing cluster found on a compromised server. The cluster consists of three services: a Redis cache, a Python API broker, and a C-based telemetry processing worker. The malicious actor attempted to scrub their tracks, leaving the system broken.

Your goal is to restore the multi-service cluster and repair the C worker's source code so its output perfectly matches an encrypted oracle we recovered.

**Phase 1: Forensics & Service Integration**
The cluster artifacts are in `/home/user/investigation`. 
1. The malicious actor deleted the Redis authentication password. Recover it by analyzing the Git repository located at `/home/user/investigation/broker-repo`. 
2. Configure the services to talk to each other. The startup script `/home/user/investigation/start_cluster.sh` launches Redis, the Python Broker (port 8080), and the C Worker (port 9000). You must update `/home/user/investigation/redis.conf` and `/home/user/investigation/broker-repo/config.json` with the recovered Redis password. 
3. The Python Broker is misconfigured and failing to route requests to the C Worker. Fix its configuration so that sending a POST request to `http://localhost:8080/process` successfully forwards the payload to the C Worker at `127.0.0.1:9000`.

**Phase 2: Floating-Point Precision Repair**
The C Worker source code (`/home/user/investigation/worker_src/worker.c`) was recovered from a deleted file fragment, but it has a subtle bug. It calculates geodetic transformations, but the malicious actor intentionally downgraded certain calculations to single-precision floating-point (`float`), causing precision loss and inaccurate telemetry targeting.
1. We have recovered a stripped, intact binary of the original working version at `/app/oracle_worker`.
2. Analyze `worker.c` and fix the floating-point precision issues so that its output is bit-for-bit identical to `/app/oracle_worker` for any given input.
3. Compile your fixed version to `/home/user/investigation/worker`. The script `/home/user/investigation/start_cluster.sh` will automatically run this executable.

Ensure your compiled `/home/user/investigation/worker` behaves exactly like `/app/oracle_worker` taking the exact same stdin inputs and producing identical stdout JSON. Once the cluster is fully running and the code is fixed, leave the services running.
You are a Site Reliability Engineer (SRE) investigating an incident where bad actors are filling our filesystem by exploiting our log ingestion API. You need to fix our multi-service setup, implement a payload filter in Go, setup a reverse proxy, and add storage monitoring.

Your objectives:

1. **Environment & Multi-Service Setup**: 
   We have two backend services located at `/app/backend1` and `/app/backend2`. They are supposed to be started via `/app/start_services.sh`. However, they are crashing or unreachable due to missing environment configuration. 
   Set the environment variables `BACKEND1_PORT=9001` and `BACKEND2_PORT=9002` permanently for the `user` shell profile (e.g., `/home/user/.bash_profile`). Ensure the services start correctly and bind to these ports on localhost.

2. **Reverse Proxy & Load Balancer**:
   Write a Go program at `/home/user/proxy.go` and compile it to `/home/user/proxy`. The program must act as an HTTP reverse proxy listening on `127.0.0.1:8080`. It must round-robin incoming HTTP requests equally between `127.0.0.1:9001` and `127.0.0.1:9002`. Run this proxy in the background.

3. **Adversarial Payload Filter**:
   Write a Go CLI tool at `/home/user/filter.go` and compile it to `/home/user/filter`. This tool will be used to sanitize incoming payloads before they hit the disk.
   The tool must take exactly one argument: the absolute path to a file containing a JSON payload.
   - It must exit with status code `1` (Reject) if the file size is greater than 10,240 bytes (10KB), or if the file contains the literal substrings `../` or `..\` anywhere in its contents (indicating a directory traversal attempt).
   - It must exit with status code `0` (Accept) if the file is well-formed JSON, under the size limit, and contains no traversal strings.

4. **Storage Monitoring**:
   Write a shell script at `/home/user/monitor.sh` that calculates the total disk usage of the directory `/home/user/logs/` in bytes. If the size exceeds 50000 bytes, it must print exactly `WARNING: QUOTA EXCEEDED` to standard output. Otherwise, it should output `OK`.

Ensure all background processes are running and properly configured before you finish.
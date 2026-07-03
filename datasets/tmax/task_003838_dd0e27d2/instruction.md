You are tasked with fixing and completing a configuration management tracking system. This system receives configuration state dumps from our server fleet, validates them using mathematical anomaly detection, and stores the latest states.

Currently, the pipeline is broken and we are receiving malformed or mathematically anomalous (potentially tampered) configurations. 

Your objectives are:

1. **Service Composition & Routing:**
   We have a multi-service setup. Nginx is running but unconfigured. Redis is running on default port 6379. 
   You must configure Nginx (running as a daemon) to listen on port 80 and reverse-proxy requests on the `/ingest` endpoint to a Go backend service that you will run on `127.0.0.1:8080`.
   Nginx configuration should be placed at `/etc/nginx/sites-available/default` (you can use `sudo` if absolutely necessary, but assume standard writable locations or user-level config where possible; actually, since you lack root, modify the provided local nginx config at `/home/user/nginx/nginx.conf` and restart the local nginx instance running under the `user` account).

2. **Mathematical Validation Filter (Go):**
   Write a Go CLI tool at `/home/user/config_filter.go` that reads a JSON configuration file and determines if it is valid. It must exit with code `0` if the configuration is "clean" (accepted) and code `1` if it is "evil" (rejected).
   
   The JSON files contain a list of objects under the key `"services"`. Each object has `"service_name"` (string), `"allocated_ram_mb"` (float64), and `"cpu_shares"` (float64).
   
   A configuration is only valid (clean) if ALL the following mathematical invariants hold:
   - Valid JSON format with the `"services"` array present.
   - The total sum of `"allocated_ram_mb"` across all services must be strictly less than or equal to `100000.0`.
   - The standard deviation of the `"cpu_shares"` across all services must be strictly less than `10.0` (to detect anomalous resource hoarding). *Note: Population standard deviation should be used.*
   
   You are provided with a training/test corpus to verify your logic:
   - Clean files are in `/app/corpus/clean/`
   - Evil files are in `/app/corpus/evil/`
   Your filter must perfectly accept all clean files and reject all evil files.

3. **Integration (Go HTTP Server):**
   Write a Go HTTP server at `/home/user/server.go` that listens on port `8080`. 
   - It should accept `POST` requests at `/ingest` with the JSON payload in the body.
   - It should write the body to a temporary file, invoke your compiled `config_filter` binary on it.
   - If the filter returns exit code `0`, it must increment a counter in Redis (key: `valid_configs_received`) and return HTTP 200.
   - If the filter returns exit code `1`, it must return HTTP 400.

Leave the Go server running in the background on port 8080 and ensure Nginx is routing traffic to it. Ensure your `config_filter.go` is perfectly tuned to the corpus.
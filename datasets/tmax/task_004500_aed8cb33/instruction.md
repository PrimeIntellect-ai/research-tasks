You are tasked with fixing a broken web architecture and deploying an intermediate Web Application Firewall (WAF) using Python. 

Currently, an Nginx reverse proxy is returning a 502 Bad Gateway when clients attempt to access the application. The system consists of an Nginx server and a vulnerable Flask backend. A startup script at `/app/start_services.sh` launches the Nginx daemon and the Flask backend.

Your objectives:
1. **Fix the 502 Error**: The Nginx configuration located at `/home/user/nginx.conf` points to an incorrect upstream port. You must modify it so that Nginx (listening on 8080) routes traffic to your intermediate Python WAF (which you will run on port 8000), rather than directly to the Flask app (which runs on 5000). 
2. **Create a Python WAF**: Write a Python script at `/home/user/waf.py` that listens on `127.0.0.1:8000` as an HTTP server. It must act as a reverse proxy, forwarding requests to the Flask backend at `127.0.0.1:5000`. 
3. **Adversarial Filtering**: The Flask app is vulnerable to specific attack payloads. Your WAF must inspect incoming POST requests. We have provided a set of clean requests in `/app/corpus/clean/` and malicious requests in `/app/corpus/evil/`. Your WAF must forward all requests that match the structure of the clean corpus, but immediately reject any request matching the evil corpus with an HTTP 403 status code. 
4. **Health Check Configuration**: Implement an endpoint at `/status` on your WAF that returns `200 OK` and the plain text "WAF OK". Modify the Nginx configuration to add a specific location block `/health` that maps to this WAF `/status` endpoint. Nginx must reload its configuration gracefully to apply these changes.
5. **Storage Monitoring**: Your WAF must append a log of all rejected requests (just the filename or payload signature) to `/home/user/waf_rejects.log`. Write a separate bash or Python script at `/home/user/monitor_quota.sh` that checks the size of this log file. If the file exceeds 1024 bytes, the script should truncate it to 0 bytes and print "Quota exceeded, log truncated".

Ensure all services are running and properly glued together.
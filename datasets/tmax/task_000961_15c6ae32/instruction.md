You are acting as a penetration tester and need to develop a custom vulnerability scanner in C++ to audit a newly deployed internal web stack. 

The target environment consists of three interconnected services running locally:
1. An Nginx reverse proxy listening on port 8080.
2. A vulnerable Flask web API running on port 5000.
3. A Redis session store running on port 6379.

Your objective is to:
1. Reconfigure the Nginx service (config located at `/app/nginx/nginx.conf`) to properly proxy requests to the Flask API (`http://127.0.0.1:5000`) and start the Nginx and Redis services using the provided `/app/start_services.sh` script.
2. Develop a high-performance C++ vulnerability scanner located at `/home/user/scanner.cpp`.
3. The scanner must perform the following tasks:
   - Perform a service audit to confirm Nginx, Flask, and Redis are reachable.
   - Scan the API endpoints (`/api/v1/auth`, `/api/v1/data`, `/api/v1/status`) routed through Nginx (port 8080).
   - The `/api/v1/auth` endpoint is vulnerable to a token leakage issue. It leaks a cryptographic hash of the admin token. Your C++ scanner must capture this hash, crack it using a provided dictionary at `/app/dict.txt` (using SHA-256), and generate the correct cleartext token.
   - Use the cracked token to authenticate to `/api/v1/data` and extract the secret flag.
4. Your C++ program must output a JSON report to `/home/user/scan_report.json` containing the cracked token, the secret flag, and a vulnerability score. 

The testing framework will evaluate your C++ scanner's detection accuracy and execution time. You must achieve a detection score (calculated by an external test script) of at least 0.95.

Compile your code to `/home/user/scanner` using `g++ -O3 -lcurl -lcrypto -pthread scanner.cpp -o scanner`. Run it to ensure `/home/user/scan_report.json` is generated correctly.
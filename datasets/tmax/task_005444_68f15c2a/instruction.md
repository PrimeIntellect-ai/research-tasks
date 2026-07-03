You are stepping in as a system administrator to fix a broken web stack. Users are reporting a "502 Bad Gateway" error when accessing the local nginx server. The previous admin left abruptly and only left behind a diagram of the architecture and a collection of HTTP request logs.

Your tasks:

1. **Identify the Backend Port:**
   There is a network architecture diagram located at `/app/architecture.png`. You must extract the correct backend port number from this image (you can use `tesseract` or similar tools). 

2. **Fix the Nginx Configuration:**
   The unprivileged nginx configuration file is located at `/home/user/nginx.conf`. It is currently misconfigured and pointing to a placeholder port. Update the `proxy_pass` directive in this file to point to the correct backend port you discovered from the image (assume localhost `127.0.0.1`).

3. **Develop a WAF (Web Application Firewall) Filter:**
   The backend was crashing due to malicious requests. You need to write a standalone C++ program that will be integrated as a pre-filter. 
   - Write your code in `/home/user/waf.cpp` and compile it to an executable at `/home/user/waf`.
   - The executable must take a single command-line argument: the path to a file containing an HTTP request payload.
   - It must read the file, analyze the payload, and return an exit code of `0` if the payload is safe, or an exit code of `1` (or any non-zero) if the payload is malicious.
   - You have been provided with two directories of sample requests:
     - `/app/corpus/clean/` contains legitimate, safe requests.
     - `/app/corpus/evil/` contains malicious requests that crash the backend.
   - Analyze these corpora to determine the patterns of malicious requests. Your compiled `/home/user/waf` program must successfully reject 100% of the files in the evil corpus and accept 100% of the files in the clean corpus.

Ensure your compiled executable `/home/user/waf` is functional and the `nginx.conf` file is correctly updated.
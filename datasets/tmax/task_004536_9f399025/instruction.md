You are an infrastructure security engineer. We are building a polyglot build system from scratch. The system allows internal developers to submit C source code via a REST API. The system compiles the C code into a shared library (`.so`), calculates a specific error-correcting checksum (CRC32), registers the build in a Redis cache, and returns the checksum.

However, we need to secure this build system. Your task involves orchestrating the microservices, setting up a CI/CD test script, and implementing a Web Application Firewall (WAF) script to analyze the C payloads before they are compiled.

### 1. Multi-Service Configuration
The application stack resides in `/app/service/` and consists of three components:
- **Redis**: Runs locally. You must ensure it is running on the default port `6379`.
- **Flask Build API**: A Python web service in `/app/service/app.py`. It needs to connect to Redis, compile incoming C code to a shared library, and return the checksum. Currently, it is misconfigured. You must fix `app.py` so that it listens on `127.0.0.1:5000` and correctly writes the shared object to `/tmp/builds/`.
- **Nginx**: You must configure Nginx to act as a reverse proxy. Create an Nginx configuration at `/etc/nginx/sites-enabled/build_api` that listens on port `8080` and proxies all requests to the Flask app on `127.0.0.1:5000`. Ensure Nginx is started and running.

### 2. Adversarial WAF implementation
Before submitting code to the build API, payloads must be statically analyzed.
Create a Python script at `/home/user/waf.py`.
- **Signature:** It must accept a file path via the CLI: `python3 /home/user/waf.py --file <path_to_json>`
- **Logic:** The JSON file contains a single key `"source_code"` mapping to a string of C source code. Your script must parse the JSON and analyze the C code.
- **Rules:** Reject any C code that attempts to invoke shell commands or execute external binaries (e.g., `system`, `popen`, `execve`, `fork`). 
- **Exit Codes:** The script must exit with status `0` if the code is clean, and exit with status `1` if it detects malicious intent. 
*Note: A corpus of clean and evil payloads will be used to evaluate your WAF script. It must achieve 100% accuracy.*

### 3. CI/CD Integration Script
Write a bash script at `/home/user/ci_cd.sh`.
This script should:
1. Accept a directory path as an argument.
2. Iterate through all `.json` files in that directory.
3. For each file, run `/home/user/waf.py --file "$file"`.
4. If the WAF exits with `0`, the script must POST the JSON file to `http://127.0.0.1:8080/build` with the `Content-Type: application/json` header.
5. Append the HTTP status code and the response body to `/home/user/build_pipeline.log`.

Start the services and ensure your WAF and CI/CD scripts are fully functional.
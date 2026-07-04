You are tasked with migrating a web security service from Python 2 to Python 3. The service exposes a REST endpoint that calculates a heavy cryptographic checksum (HMAC combined with a custom error-correcting code sequence) to validate incoming payloads.

Currently, the legacy Python 2 service is located at `/home/user/app/legacy/app.py` and runs on port 5000. It is slow and does not utilize caching. 

Your objectives are:
1. **Python 3 Migration & API Construction:** Create a new Python 3 service at `/home/user/app/v2/main.py`. It must run on port 5001. Replicate the endpoint `/verify` which accepts GET parameters `payload` and `sig`. It should return a JSON response `{"valid": true}` or `{"valid": false}` based on the exact same cryptographic logic used in the legacy application.
2. **Performance Optimization:** The legacy app calculates the checksum every time. To meet our CI/CD pipeline's performance threshold, your Python 3 service MUST cache computed valid signatures using Redis (running on `localhost:6379`, DB 0). Use the `payload` as the key and the valid signature as the value. Cache expiration is not required.
3. **Multi-Service Composition (Nginx):** Create an Nginx configuration file at `/home/user/app/nginx.conf`. It should run as a reverse proxy listening on port 8080.
   - Route requests starting with `/legacy/` to the Python 2 service (`http://127.0.0.1:5000/`). Strip the `/legacy` prefix so the upstream receives `/verify...`.
   - Route requests starting with `/v2/` to your new Python 3 service (`http://127.0.0.1:5001/`). Strip the `/v2` prefix so the upstream receives `/verify...`.
4. **CI/CD Testing Script:** Write a bash script at `/home/user/app/ci_test.sh` that makes a curl request to `http://127.0.0.1:8080/v2/verify?payload=test&sig=dummy` and saves the HTTP status code to `/home/user/app/test_status.log`.

Make sure your Python 3 service is running in the background and Nginx is started using your config. The automated verifier will blast your Nginx server on port 8080 with thousands of requests. Your Python 3 implementation must output exactly the same results as the Python 2 implementation, but achieve a significant speedup through Redis caching.
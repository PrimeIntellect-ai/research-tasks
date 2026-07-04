You are tasked with finishing a text-sanitization microservice for our web application. We have a multi-service setup consisting of Nginx, a Redis instance, and a Python Flask application. However, the system is currently broken and incomplete. 

Here is what you need to do:

1. **Fix the Python Package**: The Flask application is located in `/home/user/app/sanitizer-app`. Its `pyproject.toml` is broken (invalid syntax and missing the `redis` and `flask` dependencies). Fix it so the package can be installed via `pip install -e .`.

2. **Translate Detection Logic**: We have a legacy detection script written in JavaScript located at `/home/user/app/legacy/detector.js`. It recursively decodes input strings (handling Hex, Base64, and URL encoding) and flags malicious keywords. You must translate this logic exactly into Python and place it in `/home/user/app/sanitizer-app/sanitizer/detector.py`, exposing a function `is_malicious(text: str) -> bool`.

3. **Implement the API and Mock Tests**: In `/home/user/app/sanitizer-app/sanitizer/app.py`, use the `is_malicious` function to implement a POST endpoint `/sanitize`. It should accept JSON `{"text": "..."}` and return `{"safe": true}` if clean, or `{"safe": false}` if malicious. The app also logs requests to Redis. You must write a `pytest` test file in `/home/user/app/sanitizer-app/tests/test_app.py` that mocks the Redis connection and tests the endpoint.

4. **Service Integration**: Fix the Nginx configuration at `/home/user/app/nginx/nginx.conf` so that Nginx (listening on port 8080) correctly proxies requests to `/sanitize` to the Flask app running on `127.0.0.1:5000`. Start the services using `/home/user/app/start_services.sh`.

5. **Adversarial Verification**: Your `is_malicious` translation and endpoint will be tested against two corpora:
   - `/home/user/data/evil/` (containing text files with layered encodings of malicious payloads)
   - `/home/user/data/clean/` (containing safe text files)
   
The automated verifier will send every file's content to `http://localhost:8080/sanitize`. You must achieve 100% rejection of the evil corpus (`{"safe": false}`) and 100% acceptance of the clean corpus (`{"safe": true}`).

Leave the services running when you are finished.
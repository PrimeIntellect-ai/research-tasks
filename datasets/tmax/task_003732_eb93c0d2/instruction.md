You are an AI assistant helping a developer debug a complex build and inference pipeline. 

We have a machine learning inference system that involves multiple cooperating services. The system takes numerical requests, preprocesses them, runs an inference script via a local Python backend, and caches the results. 

The setup involves three services running locally:
1. `preprocessing_node` running on port 8001 (Node.js script that forwards data).
2. `inference_backend` running on port 8002 (Python Flask app).
3. `cache_redis` running on port 6379.

Currently, the build is failing or misbehaving due to a combination of issues:
1. The `inference_backend` contains a C-extension module (`_fast_math.c`) built via `setup.py` that is currently failing to link correctly during the build process due to a missing library flag. You need to fix the `setup.py` so the extension compiles and links.
2. Even when compiled, the Python inference logic (`inference.py`) suffers from a precision loss bug when converting float64 values from the JSON payload down to float32 before passing them to the C extension, causing outputs to deviate wildly for small values.
3. The environment variables for the Flask app to connect to Redis are misconfigured in the service startup script (`start_services.sh`), causing the cache to fail and the system to return HTTP 500s or fallback errors.

Additionally, we need a sanitiser function. The system often receives malformed or adversarial float payloads (e.g., NaN, Infinity, or out-of-bounds scientific notation strings) that crash the C extension. 
You must implement a Python sanitiser script `/home/user/app/sanitiser.py` containing a function `clean_payload(data_dict)`. It must accept a dictionary. If the payload contains valid, finite numerical data (bounds: -1e10 to 1e10), it should return the dictionary unchanged. If it contains invalid values (NaN, Inf, strings that don't parse to finite floats, or out of bounds), it must raise a `ValueError`.

Your tasks:
1. Fix the build error in `/home/user/app/backend/setup.py` so the `_fast_math` module compiles.
2. Fix the precision loss issue in `/home/user/app/backend/inference.py`. Ensure data remains as float64 when passed to `_fast_math`.
3. Fix `/home/user/app/start_services.sh` so `inference_backend` correctly connects to `cache_redis`.
4. Write the sanitiser function in `/home/user/app/sanitiser.py`.
5. Start the services using `/home/user/app/start_services.sh`.

Once you are done, create a log file at `/home/user/app/completion.log` containing exactly the string "SYSTEM_READY".
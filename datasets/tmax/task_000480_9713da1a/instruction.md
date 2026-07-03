You are a web developer tasked with optimizing a mathematical backend feature. We have a pure-Python reference implementation that generates two sequences, evaluates polynomials, and merges them in sorted order. It is currently too slow. We want to delegate the heavy lifting to a C library, wrap it in a Python Flask API, cache results in Redis, and serve it behind an Nginx reverse proxy. 

Currently, the project in `/home/user/app` is broken in several ways:

1. **C Compilation/Linking Error:** In `/home/user/app/c_src/`, there is a `poly.c` file and a `Makefile`. The Makefile is supposed to build a shared library `libpoly.so`, but it has a linking error and fails to compile properly. Fix the Makefile so `make` successfully produces `libpoly.so`.
2. **Code Translation:** The `poly.c` file contains a stub for `compute_and_merge`. Translate the logic from the Python function `compute_and_merge_ref` found in `/home/user/app/reference.py` into this C function. It must output the exact same mathematical results (double precision arrays).
3. **API Integration:** Modify `/home/user/app/api.py`. It currently exposes a Flask route `/api/merge?n=<N>&m=<M>`. Update it to:
   - Use Python's `ctypes` to load `/home/user/app/c_src/libpoly.so` and call `compute_and_merge`.
   - Implement caching: Before computing, check if the result for the given `n` and `m` is in Redis (running on `localhost:6379`) under the key `poly_merge:{n}:{m}`. If it is, return the cached JSON string. If not, compute it, store the exact JSON string in Redis with an expiration of 60 seconds, and return it.
4. **Service Configuration:** Fix `/home/user/app/nginx.conf`. It is supposed to listen on port 8080 and proxy requests for `/api/` to the Flask app running on port 5000. 
5. **Startup:** Once you have fixed the code and configurations, start the services by running `/home/user/app/start_services.sh`.

**Verification Requirements:**
Our automated test suite will send random `GET` requests to `http://localhost:8080/api/merge?n=<N>&m=<M>` where $N$ and $M$ are integers between 10 and 1000. 
The HTTP response body must be a JSON array of floats matching the exact output of `reference.py <N> <M>` bit-for-bit. 
You must ensure the Flask app returns HTTP 200, the JSON structure is identical (standard `json.dumps` without spaces, e.g., `[1.0,2.5,3.1]`), and that Redis successfully caches the responses.

Ensure all services are running and listening on their respective ports before you finish.
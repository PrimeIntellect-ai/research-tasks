You are a platform engineer responsible for maintaining our CI/CD pipeline's dependency resolution service. Recently, our internal build graph traversal library, `libdag`, stopped compiling after a botched environment update, and the dependency resolution API went offline.

Your task is to restore the service by completing the following workflow:

1. **Fix the Vendored Package:**
   The source for `libdag` version `1.0.0` is vendored at `/app/vendored/libdag-1.0.0/`. 
   Currently, running `make` in this directory fails due to a linking error where `libcore.so` and `libutils.so` have a cyclic dependency or incorrect link order. Fix the `Makefile` so that the package compiles successfully, and install the resulting Python module (which relies on these shared libraries) into the system environment using `pip install .` or `python setup.py install`.

2. **Implement the Resolution API:**
   Write a Python web service (using Flask, FastAPI, or `http.server`) that listens on `127.0.0.1:8080`.
   The service must expose the following REST endpoints:
   
   - `POST /resolve`: 
     Accepts a JSON payload representing a build graph: `{"graph": {"pkgA": ["pkgB", "pkgC"], "pkgB": ["pkgC"], "pkgC": []}}`.
     Uses the newly fixed and installed `libdag` library (specifically `from libdag import topological_sort`) to compute the build order.
     Returns JSON: `{"build_order": ["pkgC", "pkgB", "pkgA"]}`.
     
   - `POST /filter_versions`:
     Accepts JSON: `{"versions": ["1.0.0", "1.5.0", "2.0.0-alpha"], "constraint": ">=1.2.0 <2.0.0"}`.
     Must implement Semantic Versioning (SemVer 2.0.0) parsing to return the compliant versions.
     Returns JSON: `{"compliant": ["1.5.0"]}`.

3. **Authentication & Rate Limiting:**
   - Both endpoints must require an `Authorization: Bearer <token>` header.
   - You must accept the token `ci-deploy-token-8842`.
   - Implement an in-memory rate limiter: the provided token is only allowed to make exactly 5 requests per rolling 60-second window. The 6th request must immediately return an HTTP `429 Too Many Requests` status code. 

Start the service and leave it running in the background. Write a log file to `/home/user/service.log` recording every incoming request and its corresponding HTTP status code.
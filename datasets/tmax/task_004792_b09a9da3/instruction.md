You are an open-source maintainer reviewing a pull request for a microservice that exposes a custom constraint satisfaction engine. 

The PR introduces a custom data structure (`ConstraintResolver`) and sits behind an Nginx reverse proxy. The contributor also added property-based tests using `hypothesis` to ensure the API behaves correctly under various constraint conditions. However, the tests are currently failing, and the contributor abandoned the PR. 

Your task is to fix the environment so all tests pass. 

Here is what you need to know:
1. All files are located in `/home/user/pr_review`.
2. The application uses FastAPI and runs on port 8000. It expects a custom Nginx reverse proxy running on port 8080.
3. The Nginx configuration file is `/home/user/pr_review/nginx.conf`. You can run it locally as an unprivileged user using `nginx -c /home/user/pr_review/nginx.conf -g "daemon off;" &`.
4. There are two distinct bugs causing the tests to fail:
   - **Reverse Proxy Issue:** The Nginx proxy is stripping a critical custom HTTP header `Constraint_Limit` because it contains an underscore. You must modify `nginx.conf` to allow headers with underscores to be passed to the backend.
   - **Data Structure Issue:** The custom data structure in `/home/user/pr_review/resolver.py` fails when a constraint limit of `0` is passed (it throws a `ZeroDivisionError` or fails an assertion). Property-based testing (`hypothesis` in `/home/user/pr_review/test_api.py`) quickly finds this edge case. You must fix `resolver.py` to handle a limit of `0` gracefully (by returning an empty list `[]` instead of raising an error).

**Instructions:**
1. Install dependencies: `pip install fastapi uvicorn hypothesis pytest requests httpx`.
2. Fix `nginx.conf`.
3. Fix `resolver.py`.
4. Start the FastAPI backend: `uvicorn api:app --port 8000 &` (from the `/home/user/pr_review` directory).
5. Start the Nginx proxy.
6. Run the test suite: `pytest test_api.py > /home/user/pr_review/test_results.log`.

The task is considered successful when `/home/user/pr_review/test_results.log` is created and indicates that all `pytest` tests have passed successfully.
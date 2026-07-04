You are a QA engineer setting up a test environment for a new mathematical operations API. You need to build a Python package, configure a reverse proxy, and test the endpoints.

Please complete the following steps:

1. **Build a Python Package**:
   Create a Python package directory at `/home/user/math_ops`. Create a `setup.py` file to configure the build. The package must install its dependencies (e.g., `flask`) and define a console script entry point named `run-math-api`.

2. **Implement the API**:
   The package must implement a Flask application with three `POST` endpoints. They should accept and return JSON.
   - `/api/sort`: Accepts `{"data": [array of integers]}`. Returns `{"result": [array sorted in ascending order]}`.
   - `/api/merge`: Accepts `{"list1": [array], "list2": [array]}`. Returns `{"result": [merged array]}` containing all elements from both lists, combined and sorted.
   - `/api/diff`: Accepts `{"list1": [array], "list2": [array]}`. Returns `{"result": [array]}` containing the symmetric difference of the two sets of numbers, sorted in ascending order.
   
   The `run-math-api` command should start the Flask server on `127.0.0.1:5000`.
   Install the package in your environment (`pip install -e /home/user/math_ops`).

3. **Configure Nginx**:
   Create an Nginx configuration file at `/home/user/nginx.conf`. Since you do not have root access, configure the `pid` file, `error_log`, and all necessary temp paths (`client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, `scgi_temp_path`) to point to paths inside `/home/user/`.
   Configure a server listening on port `8080` that reverse proxies all requests to `http://127.0.0.1:5000`.

4. **Execution and Testing**:
   Start your Flask application in the background.
   Start Nginx in the background using your custom config (`nginx -c /home/user/nginx.conf`).
   
   Using `curl`, send the following requests to the Nginx reverse proxy (port 8080). Write the raw JSON response body for each request as a new line in `/home/user/test_results.log`.
   - Sort payload: `{"data": [10, -2, 5, 3]}`
   - Merge payload: `{"list1": [1, 5, 9], "list2": [2, 5, 8]}`
   - Diff payload: `{"list1": [1, 2, 3, 4], "list2": [3, 4, 5, 6]}`

Ensure the log file contains exactly three lines of JSON corresponding to the responses.
You are a backend developer inheriting the `geo_api` codebase located at `/home/user/geo_api`. The previous developer left the repository in a broken state, and you need to debug and fix it, then bring the service online. 

There are four specific issues you must resolve:

1. **Secret Recovery:** The API requires an authentication token to start, which should be located at `/home/user/geo_api/token.key`. The file is currently missing. The previous developer accidentally committed it to the git repository in the past, then deleted it. You must use git forensics to find the deleted token and recreate the `token.key` file with its exact original contents in the `/home/user/geo_api/` directory.

2. **Precision Loss Regression:** The API endpoints recently started suffering from severe floating-point precision loss when returning coordinate data. You must use `git bisect` (or manual git history inspection) on the `/home/user/geo_api` repository to identify the commit that introduced this precision loss regression. Once identified, fix the code in `app.py` or `processor.py` to restore the full precision of the float outputs.

3. **Vendored Package Loop Termination:** The API relies on a custom mathematics library vendored precisely at `/app/vendored/geomath`. Due to a recent faulty patch applied to this vendored package, calling the geometry processing function causes a `RecursionError` (infinite recursion). Inspect `/app/vendored/geomath/core.py`, identify the missing base case or loop termination condition, and fix it. 

4. **Service Integration:** Once the bugs are fixed, start the Python HTTP server from the `/home/user/geo_api` directory. It is configured to run using `python server.py`. 

The server must listen indefinitely on `127.0.0.1:8080`. Do not daemonize or background the process in a way that causes your script to exit; leave the server running in the foreground as your final action so it can be verified.
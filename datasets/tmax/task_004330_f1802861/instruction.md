We are experiencing a severe memory leak in our data processing microservice. The service accepts JSON payloads, applies a data transformation diff, and returns the result. 

We recently vendored a third-party library, `pydatatransform` (version 1.2.0), located at `/app/pydatatransform-1.2.0`. Since deploying this vendored version, the service's memory usage grows unbounded over time, eventually leading to OOM kills. 

Your tasks are to:
1. **Fuzz / Analyze**: Investigate the `/home/user/server.py` code and the vendored `/app/pydatatransform-1.2.0` package. Fuzz the internal functions or use data transformation diff analysis to find what specific input or logic causes the memory leak. 
2. **Create an MRE**: Create a Minimal Reproducible Example script at `/home/user/mre.py` that directly imports `pydatatransform`, executes the leaky function exactly once with a hardcoded mock payload, and exits.
3. **Fix the Leak**: Modify the source code of the vendored `pydatatransform` package in `/app/` to eliminate the memory leak. Do not alter the intended data transformation logic or its return values, only fix the resource leak.
4. **Deploy**: Start the fixed server in the background so it listens on `127.0.0.1:8888`. 

The server must successfully accept `POST` requests to `/api/v1/diff` with a JSON body formatted as `{"base": <dict>, "diff": <dict>}` and return the appropriately merged JSON dictionary. 

Leave the server running in the background when you are finished. Automated tests will verify that the memory leak is resolved by sending thousands of requests to `127.0.0.1:8888/api/v1/diff` and monitoring the process's RSS memory, followed by verifying the structural correctness of the responses.
You are a build engineer managing an artifact CI/CD pipeline. We have a legacy, stripped Linux binary at `/app/module_checker` (written in Go, utilizing concurrent goroutines for internal analysis) that verifies if specific source modules are safe to promote. We lost the source code and documentation for it.

Your task is to build a Python-based HTTP service that integrates this binary into our new pipeline. 

Requirements:
1. Create a Python HTTP server (using any standard library or framework you prefer, like `http.server`, `Flask`, or `FastAPI`) that listens on `127.0.0.1:8080`.
2. The server must expose a `POST /analyze` endpoint that accepts a raw text payload representing a multi-file Rust build log (which typically fails due to lifetime issues).
3. Implement a state machine or parser in Python to process the build log and extract the names of failing modules. A failing module is defined as the file name (without the `.rs` extension) in the line immediately following an error declaration. 
   Example log snippet:
   ```
   error[E0597]: `x` does not live long enough
     --> src/network_handler.rs:14:5
   ```
   In this case, the module name is `network_handler`.
4. For each extracted module name, figure out how to invoke the `/app/module_checker` binary to check it. You will need to inspect or interact with the stripped binary to understand its expected CLI arguments.
5. The `POST /analyze` endpoint must return a JSON response in the following format:
   ```json
   {
     "failing_modules": ["network_handler", "db_migrator"],
     "checker_results": {
       "network_handler": "REJECTED",
       "db_migrator": "APPROVED"
     }
   }
   ```
   (Where the checker results match the output or exit status interpreted from the binary).

Write the server script to `/home/user/server.py` and run it in the background so it is actively listening on port 8080.
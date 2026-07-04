You are tasked with fixing a broken CI/CD deployment of a custom C-based web service managed by a bash service runner. The deployment currently fails because the Nginx reverse proxy returns a 502 Bad Gateway when accessing the application. 

Here is the current state of the system:
1. Nginx is installed and configured via `/app/nginx/nginx.conf` to listen on `127.0.0.1:8080`. It is supposed to proxy requests to our custom backend.
2. The custom backend is a C HTTP server vendored at `/app/vendor/simple-c-server-1.0`. 
3. The CI/CD script `/app/ci_runner.sh` attempts to build the C server, start the backend, start Nginx, and run some integration tests.

However, the deployment is failing due to several issues:
- **Build Failure:** The vendored C application fails to compile. There is a typo or missing flag in the `Makefile` causing the build to fail. You need to fix the Makefile so `make` succeeds.
- **502 Bad Gateway:** Even if compiled manually, the integration test in `/app/ci_runner.sh` reports a 502 Bad Gateway. Inspect the Nginx configuration and the C application to ensure Nginx proxies to the correct port that the C server actually binds to.
- **Race Condition (Missing Dependency):** The `ci_runner.sh` script starts both Nginx and the backend simultaneously. Similar to a missing `After=` directive in systemd, Nginx fails to proxy immediately because the backend takes a few seconds to initialize. You must modify `/app/ci_runner.sh` to explicitly wait for the C backend to be listening on its port before starting Nginx. Use standard bash tools (like `ss`, `netstat`, or `nc`, and loops) to achieve this.
- **Timezone Bug:** The C application has a runtime assertion that causes it to crash immediately unless the `TZ` environment variable is explicitly set to `Etc/UTC`. Update the service runner to export this correctly before starting the backend.

**Success Criteria:**
1. Fix the Makefile in `/app/vendor/simple-c-server-1.0`.
2. Fix the upstream port configuration in `/app/nginx/nginx.conf`.
3. Fix `/app/ci_runner.sh` to set the timezone, wait for the backend to start, and then start Nginx.
4. Leave the services running in the background. Nginx must be actively listening on `127.0.0.1:8080` and returning `HTTP 200 OK` for a `GET /status` request when you are finished.

Do not change the absolute paths of the files. You may use any standard Linux tools available to fix the issues.
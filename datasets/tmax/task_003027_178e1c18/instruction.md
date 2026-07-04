You are an observability engineer tasked with setting up a custom local metrics dashboard backend for a development team.

You have been provided with a mock-up image of the dashboard specification at `/app/dashboard_config.png`. Please extract the required **Port** and **Bearer Token** from this image.

Your tasks are:

1. **Dashboard Backend implementation (C++)**
   - Write a C++ HTTP server in `/home/user/dashboard.cpp`. 
   - A single-header HTTP library is provided at `/home/user/httplib.h` (cpp-httplib) for your convenience.
   - The server must listen on `127.0.0.1` using the **Port** specified in the image.
   - Implement a single endpoint: `GET /api/metrics`.
   - This endpoint must be protected. It should only return HTTP 200 OK if the `Authorization` header exactly matches `Bearer <Token>` (using the Token from the image). Otherwise, return HTTP 401 Unauthorized.
   - When authorized, the endpoint should read the contents of `/home/user/metrics_output.json` and serve it as the response body with `Content-Type: application/json`.

2. **Cron Job Fix**
   - We need to track the number of commits in a local git repository located at `/home/user/source_repo`.
   - There is a script at `/home/user/cron_task.sh` that is supposed to count the commits and write a JSON object `{"commits": <N>}` to `/home/user/metrics_output.json`.
   - The script currently works when run interactively, but it is failing or writing to the wrong location when run via `cron` due to environment/PATH differences and missing absolute paths.
   - Fix `/home/user/cron_task.sh` so it executes reliably under cron.
   - Install the script into the user's crontab to run every minute (`* * * * *`).

3. **Execution**
   - Compile your C++ server (e.g., `g++ -O2 dashboard.cpp -o dashboard_server -lpthread`).
   - Run the server in the background so it is actively listening.
   - Ensure `metrics_output.json` is generated correctly at least once (you may trigger the script manually to seed the file).

Automated tests will issue HTTP requests to your daemon to verify the correct port, authentication, and JSON metric format.
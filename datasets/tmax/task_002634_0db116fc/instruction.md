You are a FinOps Analyst engineering an automated system to track and control wasted cloud expenditure. You need to build a pipeline that extracts billing metrics from a legacy monitoring system's visual output, enforces cost-control rules via version control, and exposes a management API.

Follow these instructions to set up the system:

1. **Extract Metrics from Video Dashboard:**
   We have a screen recording of our legacy cloud usage dashboard at `/app/dashboard.mp4`. In this dashboard, whenever the system is overprovisioned, the screen flashes solid red (RGB: 255, 0, 0).
   - Use `ffmpeg` and any scripting tools you prefer to analyze `/app/dashboard.mp4`.
   - Count the total number of pure red frames. Every red frame equates to one overprovisioned hour.
   - Save the final integer count of overprovisioned hours to a file located at `/home/user/overprovisioned_hours.txt`.

2. **Implement Git-Based Cost Controls (CI/CD Pipeline):**
   We manage our cloud deployment configurations via Git. You need to prevent engineers from manually overriding limits.
   - Create a bare Git repository at `/home/user/finops_rules.git`.
   - Create a `pre-receive` hook in this repository. 
   - The hook must inspect incoming pushes. If any newly pushed commit introduces the exact string `START_EXPENSIVE_VM` into any file, the hook must reject the push (exit with a non-zero status) and output exactly: `Cost limit exceeded`.
   - Ensure the hook is executable and correctly configured.

3. **Deploy the FinOps API Service:**
   Write a custom HTTP service (you may use Python, Node, or Bash) and run it in the background.
   - The service must listen continuously on `127.0.0.1:9090`.
   - **Endpoint 1: `GET /metrics`**
     Must return an HTTP 200 OK with a JSON payload containing the metric you extracted: `{"overprovisioned_hours": <COUNT>}` (replace `<COUNT>` with the actual integer).
   - **Endpoint 2: `POST /webhook`**
     Must enforce authentication. It should check for the HTTP header `Authorization: Bearer finops-cost-token`.
     - If the token is present and valid, return `HTTP 200 OK`.
     - If the token is missing or invalid, return `HTTP 401 Unauthorized`.

Ensure your API service is running in the background and listening on port 9090 before you finish. All files should be owned by `user` and placed under `/home/user/`.
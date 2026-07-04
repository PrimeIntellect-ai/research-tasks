You are a FinOps analyst working on optimizing cloud costs by correlating code deployments with regional cloud billing metrics. You need to implement a Git deployment hook that acts as a deployment health check. 

We have a local Git repository located at `/home/user/finops-repo`. 
A simulated local billing metric service is running on `127.0.0.1:10080`.

Your task is to write a C++ program and install it as a `post-commit` Git hook for the `finops-repo`. 

The C++ program must perform the following actions every time a commit is made:
1. **Locale & Timezone**: It must capture the current timestamp and format it in the `Asia/Tokyo` timezone, using the format `YYYY-MM-DD HH:MM:SS JST`. You must configure the timezone programmatically within the C++ code before getting the time.
2. **Health Check**: It must perform a basic TCP health check to verify if the billing service on `127.0.0.1:10080` is accepting connections. If it successfully connects, the state is `UP`; if it fails, the state is `DOWN`.
3. **Git Integration**: It must retrieve the full 40-character Git commit hash of the commit that was just made.
4. **Logging**: It must append a single line to `/home/user/cost_health.log` in the exact following format:
   `[{timestamp}] COMMIT: {commit_hash} - BILLING_SVC: {state}`
   *Example: `[2023-10-27 15:30:00 JST] COMMIT: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b - BILLING_SVC: UP`*

Instructions:
- Write your C++ source code in `/home/user/hook.cpp`.
- Compile it directly to the appropriate hook path: `/home/user/finops-repo/.git/hooks/post-commit`.
- Ensure the hook is executable.
- Once the hook is installed, create a new empty commit in `/home/user/finops-repo` (e.g., `git commit --allow-empty -m "Trigger hook"`) to execute your hook and generate the log file.
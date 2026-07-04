I need your help fixing a severe performance regression in our multi-service processing pipeline located at `/home/user/app_repo`.

The system consists of three services written in Bash:
1. `router_service` (listens on port 8000)
2. `processing_worker` (listens on port 8001)
3. `logging_service` (listens on port 8002)

To start the system, you can run `/home/user/app_repo/start_all.sh`.
Currently, when I send a request using `curl http://localhost:8000/process?data=test`, it takes over 3 seconds to complete. Previously, this took less than 0.2 seconds.

Your tasks are:
1. Write a minimal reproducible test script to measure the response time of the `/process` endpoint.
2. Use this script to `git bisect` the repository across its 200 commits to find the exact commit that introduced the performance regression. (The first commit `HEAD~200` is known to be good, and `HEAD` is bad).
3. Analyze the logs in `/tmp/service_logs/` to reconstruct the timeline and verify why the regression occurred (you will find a binary utility `data_hasher` was replaced or improperly configured, or an artificial delay was introduced in the bash scripts).
4. Reconfigure the services in `router_config.env` and apply a patch to the current `HEAD` so that the end-to-end flow works correctly and the performance is restored. 
5. Save your final patch file to `/home/user/fix.patch` and ensure the services are running with the fix applied.

The automated verification will measure the response time of the system using a specific payload. You must ensure the response time is well below the threshold.
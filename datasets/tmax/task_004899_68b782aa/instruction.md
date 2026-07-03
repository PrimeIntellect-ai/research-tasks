You are an AI assistant acting as a container specialist managing microservices. We have a custom lightweight CI/CD webhook service vendored at `/app/vendored_ci_runner-1.2.0`. This service is intended to handle incoming deployment webhooks and execute rolling deployments for our applications. 

However, the service has a known issue: its internal job scheduler runs but fails to write deployment logs to the correct location because of a hardcoded, broken `PATH` issue in its Python source. When it attempts to execute the simulated deployment shell script, it fails or writes to an incorrect default directory rather than `/home/user/deploy_logs/`.

Your task involves the following steps:
1. Examine the vendored package in `/app/vendored_ci_runner-1.2.0`. Find the perturbation in the Python source code where the background deployment task is spawned. Fix the environment variables (specifically `PATH` and the working directory) so that the deployment jobs successfully execute and output their logs to `/home/user/deploy_logs/`.
2. Once patched, start the CI/CD webhook service. It must listen on `127.0.0.1:8080`.
3. The service exposes a webhook endpoint at `/api/v1/deploy`. To test your fix, the service must remain running in the background. Ensure the service authenticates requests using the token `DeployerToken-99x`.
4. Ensure the `/home/user/deploy_logs/` directory exists and has the correct permissions for the runner to write to it.

Once you have completed the fix and started the service on port 8080, write a confirmation message "SERVICE_READY" to `/home/user/status.txt`. The automated verifier will then send an HTTP POST request to `http://127.0.0.1:8080/api/v1/deploy` with the required authorization header to verify that the rolling deployment is triggered and that the log file is successfully created in `/home/user/deploy_logs/`.
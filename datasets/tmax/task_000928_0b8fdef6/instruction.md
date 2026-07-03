We are dealing with a deployment issue in our local mock Kubernetes environment. We have a custom C++ operator tool that manages deployment manifests, enforces disk quota policies based on user groups, and triggers a backup strategy through a local CI/CD runner. 

Currently, we have an infrastructure composed of three local services running under `/home/user/services/`:
1. A mock Kubernetes API server (running on port 8080)
2. A local metrics and quota service (running on port 8081)
3. A backup storage sink (running on port 8082)

Unfortunately, the source code for our custom manifest parser and validator (`manifest_checker`) was lost, but we have a stripped binary (`/home/user/bin/manifest_checker_ref`) that is used in our current CI/CD pipeline. 

Your task is to:
1. Re-implement the `manifest_checker` in C++. The source code should be saved at `/home/user/workspace/manifest_checker.cpp` and compiled to `/home/user/workspace/manifest_checker`.
2. The program must take exactly two arguments: the path to a JSON manifest file and the path to an output file. 
3. The program's behavior, parsing logic, and output must be bit-exact equivalent to the `/home/user/bin/manifest_checker_ref` binary for any given JSON manifest input.
4. You must also fix a broken cron job located at `/home/user/cron/backup_job.sh`. It currently attempts to run the manifest checker and trigger a backup, but it's writing to the wrong location due to missing PATH and environment variables. Ensure it writes its output to `/home/user/backups/manifest.log` and correctly calls the backup service on port 8082.
5. Reconfigure the services in `/home/user/services/docker-compose.yml` (or equivalent startup scripts) so that the CI/CD runner can correctly communicate with the mock API server and the quota service.

The automated verification will fuzz your compiled C++ program against the reference binary with thousands of generated manifests to ensure bit-exact equivalence. It will also trigger the end-to-end flow by running the fixed cron job and asserting that the backup storage sink receives the correct payload.
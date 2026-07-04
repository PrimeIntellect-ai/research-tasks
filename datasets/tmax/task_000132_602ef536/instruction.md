You are tasked with configuring a high-performance Kubernetes operator pipeline that manages manifests via Git. 

A multi-service environment is already running in the background, started from `/app/start_services.sh`. It includes:
1. A local Git HTTP server and bare repository located at `/home/user/gitserver/manifests.git` (accessible via `http://127.0.0.1:8000/manifests.git`).
2. A Mock Kubernetes API server listening on `http://127.0.0.1:9090`.

Your objectives:
1. **Develop a Git Hook in C**: 
   Write a `post-receive` hook in **C** for the bare repository at `/home/user/gitserver/manifests.git`. 
   The hook must read from standard input. For each line of the format `<old-hash> <new-hash> <refname>`, it must determine which `.yaml` files were added or modified in the push.
   For each added/modified `.yaml` file, the C program must read the file's contents at `<new-hash>` and send an HTTP POST request to `http://127.0.0.1:9090/apply` with the raw file contents in the body and `Content-Type: application/yaml`.
   Compile your C program and place the executable at `/home/user/gitserver/manifests.git/hooks/post-receive`. Ensure it has the correct permissions.

2. **Performance Requirement (Metric Threshold)**:
   Because this repository acts as a central operator for a massive cluster, performance is critical. The verifier will measure the execution time of pushing 500 YAML files. Your C-based hook must process and POST all 500 files to the API such that the entire `git push` completes in under **1.5 seconds**. You may use `libcurl` or raw sockets for the HTTP POST.

3. **Scheduled Synchronization**:
   Configure a scheduled task using `cron` (for the current user) that runs every minute. The task must execute an HTTP GET request to `http://127.0.0.1:9090/sync` and append the output (along with a newline) to `/home/user/sync.log`.

Ensure your C code handles errors gracefully and operates within the performance threshold. Do not use external command wrappers (like `system("curl ...")`) in your C code, as the overhead will likely cause you to fail the performance threshold.
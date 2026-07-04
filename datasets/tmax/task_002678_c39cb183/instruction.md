You are a deployment engineer tasked with rolling out the new `sys-exporter` metrics service on a Linux deployment server. 

Your tasks are to fix the broken vendored source code, set up a user-space mount for its data source, configure the required environment variables, and run the service.

Here are your instructions:

1. **Fix and Compile the Vendored Package:**
   We have vendored the source code for `sys-exporter-1.2.0` in the directory `/app/sys-exporter-1.2.0`. 
   - The original developer left a typo in the C++ code regarding the environment variable used to locate the target directory. It should look for `TARGET_DIR`, but currently it's broken. 
   - Additionally, the `Makefile` is failing to compile because it's missing a crucial compiler flag needed for multithreading. 
   - Fix the code and the `Makefile`, then compile the application.

2. **Mount the Data Source:**
   - The metrics data is packaged in an archive located at `/app/metrics_bundle.tar.gz`.
   - You do not have root privileges. Use `archivemount` (a user-space FUSE tool) to mount this archive read-only to `/home/user/mnt_data`. Create the mount directory if it doesn't exist.

3. **Environment Setup:**
   - The `sys-exporter` service requires two environment variables:
     - `SERVER_PORT` must be set to `8080`.
     - `TARGET_DIR` must be set to `/home/user/mnt_data`.
   - Add these exports to your `/home/user/.profile` to ensure they persist for future shell sessions.

4. **Scheduled Task / Service Execution:**
   - Configure a cron job for the `user` account that executes a startup script at `@reboot`. 
   - The startup script should be located at `/home/user/start_exporter.sh` and should:
     1. Source `~/.profile`.
     2. Ensure the `archivemount` is established.
     3. Start the compiled `sys-exporter` binary in the background.
   - For the purpose of this immediate deployment, also manually run your startup script so the service is actively listening in the background.

The final state should have the `sys-exporter` process running, listening on port 8080, and successfully serving the contents of the mounted archive over HTTP. If you run `curl http://127.0.0.1:8080/system_stats.json`, it should return the data from inside the tarball.
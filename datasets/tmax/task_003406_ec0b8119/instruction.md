You are tasked with building a local Git-based configuration operator that acts similarly to a Kubernetes operator by watching for manifests and applying network routing configurations. However, it must feature a specific "silent rejection" mechanism.

Please perform the following steps in the `/home/user` directory:

1. Initialize a new standard (non-bare) Git repository at `/home/user/manifest-repo`.
2. Write a C++ program located at `/home/user/operator.cpp` and compile it to `/home/user/operator`. This program will act as our configuration operator.
3. The C++ operator must do the following when executed:
   - Read the file `network-manifest.conf` in its current working directory.
   - Look for a line starting with `default_route=`.
   - If the route value is exactly `192.168.1.254`, it should create/overwrite the file `/home/user/active_network.log` with the exact text `ROUTE_ACCEPTED\n`.
   - If the route value is anything else, it must SILENTLY reject it. To do this, it must append the exact string `ALERT: Invalid route [VALUE] rejected\n` (where `[VALUE]` is the parsed IP address) to the simulated email spool file at `/home/user/mail_spool.txt`.
   - In all cases (even on rejection or if the file is missing), the C++ program must exit with a status code of `0`. This ensures the upstream processes don't break.
4. Create a Git hook in the `/home/user/manifest-repo` repository that automatically executes the `/home/user/operator` binary every time a commit is finalized (`post-commit`). Make sure the hook has the correct permissions.
5. Inside the Git repository, create a file named `network-manifest.conf` containing exactly one line: `default_route=10.0.0.1`.
6. Add and commit this file to the repository with the commit message "Add initial network manifest".

Your final system state should have the repository set up, the C++ operator compiled and working, the hook executable, and the commit successfully executed, which should trigger the hook and populate `/home/user/mail_spool.txt` with the alert.
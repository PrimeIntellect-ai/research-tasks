You are a backup operator tasked with testing the restoration procedures for a critical Git server. You need to verify that a repository backup can be successfully restored, that its server-side hooks execute properly with specific timezone constraints, and that it can be accessed through a proxied connection.

You have been provided with a repository backup at `/home/user/backup.tar.gz`. 

Perform the following tasks:

1. **Extraction and Directory Structure:**
   - Extract the contents of `/home/user/backup.tar.gz` into `/home/user/extracted`.
   - Create a new bare Git repository at `/home/user/bare_repo.git` using the contents of the extracted repository.
   - Create a directory `/home/user/restore_env`.
   - Inside `/home/user/restore_env`, create a symbolic link named `current_repo` that points to `/home/user/bare_repo.git`.

2. **Git Hook and Timezone Configuration:**
   - Create a `post-receive` hook in the bare repository (`/home/user/restore_env/current_repo/hooks/post-receive`).
   - The hook must append a line to `/home/user/restore_log.txt` every time a push is received.
   - The appended line MUST strictly match this format: `RESTORE_PUSH: <new_commit_hash> at <YYYY-MM-DD HH:MM:SS>` (where `<new_commit_hash>` is the full 40-character SHA-1 of the newly pushed commit).
   - **Crucial:** The timestamp logged by the hook must be evaluated in the `Pacific/Auckland` timezone, regardless of the system's global timezone settings.

3. **Service and Port Forwarding (SSH tunneling/Proxy):**
   - Start a `git daemon` to serve the `/home/user/bare_repo.git` directory locally. Configure it to listen on `127.0.0.1` port `9418`. Save the PID of the `git daemon` process to `/home/user/git_daemon.pid`.
   - Create a local TCP port forward/proxy so that any traffic sent to `127.0.0.1` port `8080` is forwarded to `127.0.0.1` port `9418`. You may use any language or tool available (e.g., Python, socat, bash) to achieve this. Run this proxy in the background and save its PID to `/home/user/proxy.pid`.

4. **Testing the Restore:**
   - Clone the repository via your port forward (i.e., from `git://127.0.0.1:8080/`) into `/home/user/test_clone`.
   - Inside `/home/user/test_clone`, create a new file named `restore_verified.txt` with the exact contents: `RESTORE OK`.
   - Add, commit, and push this new file back to the bare repository through the proxied connection. 

Leave the `git daemon` and your proxy process running when you complete the task so the testing framework can verify them.
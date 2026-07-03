You are an Site Reliability Engineer (SRE) tasked with wrapping an old, undocumented uptime monitoring binary into a modern, multi-protocol service using C. We are transitioning to a GitOps deployment model.

We have a legacy monitoring tool provided as a stripped binary at `/app/legacy_monitor`. Due to a historical bug (similar to how cron jobs often fail due to missing environment variables), this binary crashes or outputs garbage unless it is executed with a very specific environment: `TZ=America/New_York` and `LC_ALL=C`. Furthermore, it only works if `PATH` explicitly includes `/usr/local/sbin`.

Additionally, this binary checks the heartbeat of a legacy virtual machine. You must first start this VM using QEMU.
An image is provided at `/app/legacy_vm.qcow2`. You must run QEMU in the background (using `qemu-system-x86_64`) with no graphics (`-nographic`), and expose a QMP (QEMU Machine Protocol) socket at `/tmp/legacy_qmp.sock` (the stripped binary hardcodes this path to check the VM state).

Your objective is to build a C-based network daemon that wraps this binary and deploy it via a Git hook.

Step 1: QEMU Setup
Start the QEMU VM in the background using `/app/legacy_vm.qcow2`. Ensure the QMP socket is available at `/tmp/legacy_qmp.sock`.

Step 2: The Wrapper Daemon (C)
Write a C program that runs as a daemon. It must:
1. Listen on TCP port 8040 for Raw TCP connections. When it receives the string `PING\n`, it should execute `/app/legacy_monitor` (ensuring the correct environment variables are set) and send the exact stdout of the binary back to the client, followed by closing the connection.
2. Listen on TCP port 8080 for HTTP connections. When it receives a `GET /uptime HTTP/1.1` request, it should execute the binary (with the correct environment) and return a valid HTTP 200 response where the body is purely the stdout of the binary.

Step 3: Staged Deployment via Git
We want this daemon to be deployed automatically.
1. Create a bare Git repository at `/home/user/monitor.git`.
2. Configure a `post-receive` hook in this repository.
3. The hook must checkout the latest code to `/home/user/deploy`, compile the C code (using `gcc`), and restart the daemon. (You can kill the old daemon process in the hook before starting the new one).
4. Commit your C code to a local clone of this repository and push it to the bare repository to trigger the deployment.

Leave the daemon running. Automated verification will connect to ports 8040 and 8080 to test the multi-protocol responses, and will simulate code updates via git push.
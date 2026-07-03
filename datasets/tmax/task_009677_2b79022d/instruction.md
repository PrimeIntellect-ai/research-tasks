You are a systems engineer investigating why a custom user-level "VNC Bridge" service is failing to start. The service is invoked via a runner script located at `/home/user/run_bridge.sh`. 

This service consists of a C program (`/home/user/src/vnc_bridge.c`) that reads a configuration file (`/home/user/config.json`), connects to a local SSH tunnel, and communicates with a QEMU VNC server. Currently, the service crashes or fails to connect.

Your objectives are to diagnose and fix the multi-layered issues preventing the service from starting:

1. **Permission/ACL Issue:** The C program fails to read `/home/user/config.json`. Standard Linux permissions look correct, but there is an underlying Access Control List (ACL) issue blocking the `user` account from reading it. Diagnose and remove the blocking ACL so the file is readable.
2. **SSH Tunneling & Expect Scripting:** The C program expects to connect to a VNC server via a local SSH tunnel on port `5901`, which forwards to a QEMU VNC server running on port `5900`. 
   - A local SSH server is running on port `2222`. 
   - The user `user` has the password `vncpass`.
   - Write an Expect script at `/home/user/start_tunnel.exp` that non-interactively establishes an SSH local port forward (mapping local `5901` to `127.0.0.1:5900`) via `localhost` on port `2222`. 
   - Run the Expect script in the background to keep the tunnel open.
3. **C Code Debugging:** The C program `/home/user/src/vnc_bridge.c` has a bug where it hardcodes the connection port to `5900` instead of reading the `tunnel_port` from the configuration or using the correct forwarded port `5901`. Modify the C code to connect to `5901` (or parse it properly), recompile it to `/home/user/bin/vnc_bridge` using `gcc`.
4. **QEMU Verification:** Ensure a dummy QEMU instance is actually listening on VNC port 5900. If it's not running, start a minimal headless instance: `qemu-system-x86_64 -display vnc=127.0.0.1:0 -m 64 -nodefaults -daemonize`.
5. **Final Output:** Once the service runs successfully using `/home/user/run_bridge.sh`, it will generate a success message. Create a file called `/home/user/diagnostic_report.txt` containing exactly two lines:
   - Line 1: The exact error string returned by `getfacl` or the specific ACL entry that was blocking access (e.g., `user:user:---`).
   - Line 2: The exact MD5 checksum of the newly compiled `/home/user/bin/vnc_bridge` binary.

Ensure your expect script is robust and leaves the tunnel running.
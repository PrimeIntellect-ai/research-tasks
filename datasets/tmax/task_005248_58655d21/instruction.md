You are tasked with fixing and deploying a local project organization daemon, `bash-backup-daemon`, which receives compressed backup streams over the network and extracts them into a designated project directory.

Currently, the source code for this third-party package is vendored at `/app/bash-backup-daemon-1.2.0`. However, the package has a few issues that prevent it from functioning correctly, and it lacks critical security checks.

Your objectives:

1. **Fix the Vendored Package**:
   - The package uses a `Makefile` to install scripts. However, it currently tries to install to a system directory requiring root access, and has a syntax error in its environment setup file (`config.env.template`).
   - Modify the configuration so it installs locally to `/home/user/daemon-bin/`.
   - Fix the broken variable export in the startup script.

2. **Patch the Path Traversal Vulnerability (Zip Slip)**:
   - The daemon relies on the `extract_stream.sh` bash script to process incoming `tar.gz` streams. 
   - Currently, it extracts blindly. You must modify `extract_stream.sh` to add an archive integrity and security check BEFORE extraction.
   - The script must read the incoming stream, list the contents (e.g., using `tar -tzf`), and check for any file paths containing `../` or starting with `/`.
   - If a malicious path is detected, the script must abort the extraction, discard the stream, and output exactly the string `ERROR: Path traversal detected` to standard out.
   - If the archive is safe, it should extract the contents into `/home/user/projects/extracted/`.

3. **Run the Service**:
   - Start the daemon using its built-in runner (`start_daemon.sh`). It uses `socat` to listen for incoming TCP connections.
   - Configure it to listen on exactly **TCP port 8080**.
   - The daemon must remain running in the background so it can process incoming archives.

Ensure that your modified service correctly accepts valid tar.gz streams sent via raw TCP to port 8080, extracts them, and actively rejects streams containing directory traversal attempts with the required error message.
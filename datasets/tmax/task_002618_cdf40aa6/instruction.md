You are tasked with fixing and deploying a vendored archive-processing service for a development team. The service receives uploaded tar archives and extracts them into a project directory. 

The service source code is located at `/app/archive-service-1.2.0`. 
Currently, the service has several issues:
1. **Broken Build/Install**: The `Makefile` has a misconfiguration. It attempts to install binaries to a root-owned directory. You must fix it so that running `make install` installs the application to `/home/user/service_root`.
2. **Configuration Interpretation**: The service relies on a `config.ini` file. The provided script `run.sh` incorrectly reads the configuration. You must update the service so it correctly parses `config.ini` to determine the `UPLOAD_DIR` and the `PORT` to listen on. Set the service to listen on `127.0.0.1:8888` and extract files to `/home/user/service_root/uploads`.
3. **Zip Slip Vulnerability**: The core extraction logic (implemented in the vendored code) is vulnerable to "zip slip"—archives containing paths with `../` or absolute paths can overwrite files outside the target `UPLOAD_DIR`. You must modify the extraction process to sanitize or safely extract archives, ensuring no files are written outside the configured `UPLOAD_DIR`, while preserving safe symbolic and hard links within the extraction root.
4. **Concurrency and Streaming**: The extraction must support concurrent uploads safely. Implement file locking (e.g., using `flock` or equivalent mechanisms) around the extraction process so that concurrent extractions to the same target directory do not corrupt each other. Ensure the archive is processed via streaming I/O (extracted directly as it is read) rather than buffering the entire file to disk first.

**Requirements**:
- Investigate and fix the vendored package at `/app/archive-service-1.2.0`.
- After fixing, run `make install`.
- Start the service so it listens for HTTP POST requests at `127.0.0.1:8888/upload` and HTTP GET requests at `127.0.0.1:8888/files/<filename>`.
- The service must gracefully reject or safely skip malicious paths in uploaded tar files without crashing.
- Leave the service running in the background. Do not exit the terminal.

Ensure your modifications correctly handle concurrent requests and strictly prevent path traversal.
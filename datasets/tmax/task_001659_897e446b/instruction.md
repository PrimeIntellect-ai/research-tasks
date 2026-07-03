You are an observability engineer tasked with tuning a metrics processing pipeline. Our dashboard is currently broken because the custom C-based log exporter is failing to connect to the correct upstream Unix socket (much like an nginx 502 error due to a wrong upstream path). Furthermore, the pipeline is too slow and times out in our CI/CD environment.

We received a screenshot of the architecture spec in `/app/dashboard_spec.png`. You must extract the required configurations from this image.

Your objectives:
1. **Fstab Configuration**: The image specifies a `tmpfs` mount that should be added to `/etc/fstab` to host the socket. Since you do not have root access to modify `/etc/fstab`, extract the exact line specified in the image and save it into a new file at `/app/fstab_entry.txt`.
2. **Fix the C Exporter**: We have the source code for the exporter at `/app/exporter.c`. 
   - Update the hardcoded `SOCKET_PATH` in the code to match the correct socket path shown in the image.
   - The exporter has a severe performance bottleneck making it artificially slow. Identify and remove this bottleneck so it can process logs efficiently.
   - Compile the fixed code to an executable at `/app/exporter`.
3. **Log Processing Pipeline**: Create a shell script at `/app/pipeline.sh` (ensure it is executable) that acts as the primary data pipeline. The script must:
   - Read the log file located at `/app/access.log`.
   - Use standard text processing tools (`grep`, `awk`, or `sed`) to filter out all log lines that contain a `404` HTTP status code (e.g., `" 404 "`).
   - Pipe the filtered logs directly into the `/app/exporter` binary.
4. **Performance Target**: The entire `/app/pipeline.sh` script must execute and complete in under 0.5 seconds. 

Please ensure all paths, compiled binaries, and output files are exactly as specified above. You may use `tesseract` to read the text from the image.
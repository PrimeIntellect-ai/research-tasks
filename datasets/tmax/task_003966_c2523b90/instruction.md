You are tasked with cleaning up a disorganized project directory, archiving it, and serving the archive over a local HTTP server for automated retrieval.

Your objectives:
1. **Clean the Data**: In the directory `/home/user/projects/`, there are various source files, backups, and configuration files. 
   - Recursively find and delete all files ending in `.bak`.
   - Recursively find all files named `settings.conf` and use `sed` to replace any line starting exactly with `SECRET_TOKEN=` to instead read `SECRET_TOKEN=REDACTED`. Keep the rest of the file intact.

2. **Archive the Project**: 
   - Create a directory `/home/user/www/`.
   - Compress the cleaned `/home/user/projects/` directory into a gzip-compressed tarball located at `/home/user/www/clean_projects.tar.gz`. Ensure the internal paths in the tarball are relative to `/home/user/projects/` (e.g., extracting it should yield the contents, not an absolute path structure).

3. **Fix the Vendored Server**: 
   - We have provided a vendored Bash-based HTTP server package in `/app/bash-serve/`. 
   - However, the main script `/app/bash-serve/serve.sh` contains a deliberate syntax/command perturbation that prevents it from running successfully. You must identify and fix the bug in this script (hint: look at how the listening tool is invoked).

4. **Serve the Archive**:
   - Run the repaired `/app/bash-serve/serve.sh` so that it listens on `127.0.0.1:8080` and serves the contents of `/home/user/www/`.
   - Keep this server running in the background. The automated testing suite will connect to `http://127.0.0.1:8080/clean_projects.tar.gz` to verify your work.
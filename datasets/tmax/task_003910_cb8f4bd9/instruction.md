You are an artifact manager tasked with curating a local binary repository. 

Our local artifact pipeline consists of three services running on this machine:
1. An Nginx reverse proxy listening on port 8080.
2. A Flask upload API.
3. A Redis queue (standard port 6379) and a background worker.

Currently, the pipeline is broken because of misconfigurations introduced during a recent migration. The Nginx configuration (`/app/nginx.conf`) and the Flask API environment configuration (`/app/.env`) have incorrect ports, preventing end-to-end uploads from working. 

Your tasks are to:
1. **Fix the Pipeline**: Inspect the service configurations in `/app/`. Fix the Nginx upstream to point to the correct Flask port (which is bound to 5000), and fix the Flask `.env` to point to the correct Redis port. Once fixed, apply the changes by running `/app/restart_services.sh`.
2. **Parse and Curate Artifacts**: You have a backlog of 50 unoptimized ELF binaries located in `/home/user/artifacts/backlog/`. For each ELF file:
   - Extract the architecture type from the ELF header (e.g., x86-64, ARM, AArch64) using command-line parsing tools.
   - Strip all debug symbols from the binary to minimize its file size.
   - Rename the file following the bulk naming convention: `arch_<architecture_string>_<original_filename>`. (Replace any spaces in the architecture string with hyphens).
3. **Ingest**: Write a short script to loop through your optimized, renamed binaries and upload them to the system via the Nginx endpoint using standard stream tools (e.g., `curl -F "file=@<filepath>" http://127.0.0.1:8080/upload`). 

The background worker will automatically move successfully uploaded artifacts to `/home/user/artifacts/final/`. You must ensure that all 50 artifacts are uploaded and that their total disk footprint is minimized.
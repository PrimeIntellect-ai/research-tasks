You are a technical writer tasked with organizing and securing a massive documentation system. Your documentation platform relies on a multi-service pipeline that ingests, filters, serves, and backs up markdown files. 

The system consists of three cooperating services running locally:
1. **Doc-Uploader API**: A Flask application listening on port 5000 that receives markdown files.
2. **Doc-Viewer**: An Nginx web server listening on port 8080 that serves the documentation.
3. **Doc-Archiver**: A backup service listening on port 5001 that expects incremental diffs of the documentation.

However, the pipeline is currently broken and insecure. You must complete the following objectives:

### 1. Create a C-based Document Filter
Your platform frequently receives malicious uploads attempting path traversal. You must write a C program and compile it to `/home/user/doc_filter`. 
- The program will be invoked via CLI with a single argument: the path to a markdown file (e.g., `./doc_filter /path/to/file.md`).
- It must read the file and scan for markdown links: `[some text](target_path)`.
- **Evil files**: Reject the file (exit code 1) if *any* link target starts with `/` (absolute path) or contains `../` (path traversal).
- **Clean files**: Accept the file (exit code 0) if all link targets are simple relative paths (e.g., `file.md`, `images/pic.png`).
- To help you test, we have provided two corpora of files: `/home/user/corpora/clean/` (which must all be accepted) and `/home/user/corpora/evil/` (which must all be rejected).

### 2. Pipeline Configuration and Glue
You must reconfigure the services so the end-to-end flow works:
- **Uploader Configuration**: Edit `/home/user/services/uploader/config.json`. Set `"FILTER_BIN"` to the absolute path of your compiled C program (`/home/user/doc_filter`). Set the `"PUBLISH_DIR"` to `/home/user/docs_published`.
- **Nginx Configuration**: Modify `/home/user/services/nginx/nginx.conf` so that the server block for port 8080 serves files directly from `/home/user/docs_published`.
- **Backup Configuration**: The uploader parses a config file for its differential backup destination. Set `"BACKUP_URL"` in `config.json` to `http://127.0.0.1:5001/backup`.

### 3. File Operations & Linking
The Uploader service relies on a specific directory structure. You must manually create:
- `/home/user/docs_published/`
- Inside `/home/user/docs_published/`, create a symbolic link named `index.md` pointing to `/home/user/docs_published/home.md` (which will be created by the uploader later).

Start the services using `/home/user/services/start_all.sh` (this script is already written for you, but you must fix the configurations first). 
The automated verifier will simulate uploads to port 5000 and expect port 8080 to serve the approved files, while rejecting malicious ones. Ensure your C filter is robust and correctly handles edge cases in link parsing.
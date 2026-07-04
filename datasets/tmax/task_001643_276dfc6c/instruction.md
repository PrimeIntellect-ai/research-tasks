You are tasked with building a secure Artifact Curator service in Go for managing proprietary binary repositories. A legacy, closed-source extraction tool is used to analyze these binaries, but it is known to be vulnerable to "zip-slip" (path traversal) attacks when extracting files. Your service must act as a protective gateway.

You are provided with a stripped binary at `/app/extractor`. This tool analyzes `.pkg` archive files. When run as `/app/extractor --analyze <file_path>`, it outputs a multi-line log detailing the archive's contents.

Your goal is to write and run a Go web service that safely processes uploads, parsing the legacy tool's output to block malicious archives before they enter the repository. 

### Requirements

**1. Service Setup:**
* Your Go service must listen for HTTP traffic on `0.0.0.0:8080`.
* Ensure your service is running and remains running (do not exit) once you consider the task complete.

**2. Endpoint: `POST /upload`**
* Accepts a raw binary payload in the request body (the archive).
* **Atomic Staging:** Write the payload to a temporary file inside `/home/user/staging/`. You must handle file creation safely to avoid race conditions.
* **Analysis:** Execute `/app/extractor --analyze <temp_file_path>`. The extractor outputs multi-line records in the following format:
  ```
  === ARCHIVE ENTRY ===
  Filepath: <path>
  Size: <bytes>
  Type: <file|dir>
  =====================
  ```
* **Zip-Slip Prevention (Log Parsing):** Parse the output. If *any* `Filepath` contains path traversal sequences (e.g., `../`, `..\\`) or is an absolute path (starts with `/`), the archive is malicious.
* **Resolution:** 
  * If malicious: Delete the temporary file immediately and return an HTTP `406 Not Acceptable` status code.
  * If safe: Atomically move/rename the file into `/home/user/repository/`, naming it `<sha256_hash_of_file_contents>.pkg`. Return an HTTP `201 Created` status code.

**3. Endpoint: `GET /audit`**
* Performs a metadata-based search across the stored repository.
* Scan `/home/user/repository/` for all `.pkg` files.
* For each file, run the `/app/extractor --analyze` command again.
* Aggregate a list of all unique `Filepath` values found across *all* safe archives currently in the repository.
* Return an HTTP `200 OK` status. The response body must be a JSON array of strings containing these unique filepaths, sorted alphabetically.

**Initialization:**
Create the `/home/user/staging/` and `/home/user/repository/` directories before starting your service. Write your Go code in `/home/user/curator.go` and run it. You may use standard Go library packages.
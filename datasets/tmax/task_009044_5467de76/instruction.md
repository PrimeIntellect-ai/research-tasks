You are a compliance analyst generating an audit trail for a legacy file upload service. Recent security logs indicate potential path traversal attempts. You need to build a hybrid automated auditing tool using C and standard shell utilities to analyze the request logs, verify uploaded file integrity, and validate client certificates.

In the directory `/home/user/audit_data/`, you will find:
- `requests/`: Contains raw HTTP POST request logs (e.g., `req1.txt`, `req2.txt`).
- `uploads/`: Contains the actual files that were saved to the disk.
- `certs/`: Contains client certificates provided with each request (e.g., `req1.pem`, `req2.pem`) and the Root CA `ca.pem`.
- `manifest.txt`: Contains the expected SHA256 hashes for the uploads in the format `<sha256>  <basename_of_file>`.

Perform the following tasks:

1. Write a C program at `/home/user/audit_parser.c` that parses a given HTTP request text file. 
   - The program should take the file path as its first command-line argument.
   - It must extract the session cookie value from the header: `Cookie: session_id=<value>`
   - It must extract the filename from the header: `Content-Disposition: form-data; name="file"; filename="<value>"`
   - It must determine if the extracted filename contains a path traversal attempt (specifically, if it contains the substring `../`).
   - The program must print exactly one line to standard output in this format: `<session_id>,<extracted_filename>,<traversal_detected>` where `<traversal_detected>` is `1` if `../` is present, and `0` otherwise.
   - Compile this program to `/home/user/audit_parser`.

2. Write a bash script at `/home/user/generate_audit.sh` that iterates through all request files in `/home/user/audit_data/requests/` in alphabetical order. For each request:
   - Run the C program to get the session ID, filename, and traversal status.
   - Check if the corresponding certificate (`/home/user/audit_data/certs/<request_name>.pem`) is validly signed by `/home/user/audit_data/certs/ca.pem` using `openssl verify`.
   - Check if the actual uploaded file in `/home/user/audit_data/uploads/` (using the *basename* of the extracted filename, since the server strips directories when saving) matches the expected SHA256 hash in `/home/user/audit_data/manifest.txt`.
   
3. The bash script must output a final CSV log file at `/home/user/final_audit.csv` with the following header:
   `Request,SessionID,Filename,TraversalAttempt,CertValid,HashMatch`
   
   For each request, append a row. 
   - `Request`: The base name of the request file (e.g., `req1.txt`).
   - `SessionID`, `Filename`, `TraversalAttempt`: The exact values parsed by your C program.
   - `CertValid`: `true` if `openssl verify` succeeds, `false` otherwise.
   - `HashMatch`: `true` if the calculated SHA256 hash of the saved file matches the one in `manifest.txt`, `false` otherwise.

Ensure your C program is robust against typical HTTP header formatting (e.g., handles carriage returns `\r\n`). Run your script so that `/home/user/final_audit.csv` is fully populated.
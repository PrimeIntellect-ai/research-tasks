You are tasked with building a custom, lightweight "manifest operator" that mimics Kubernetes operator behavior for a proprietary cluster manager. 

An undocumented, stripped compiler binary has been provided at `/app/manifest_compiler`. This binary is used to validate and compile YAML manifests into our proprietary format. You will need to reverse-engineer its expected input format and behavior by experimenting with it (tools like `strings`, `objdump`, or black-box testing are available). It takes a single file path as an argument.

Your objective is to complete the following tasks:

1. **Write a Webhook Operator in C**: 
   Create a C program at `/home/user/operator.c` and compile it to `/home/user/operator`. 
   This program must act as an HTTP server listening on `127.0.0.1:8080`.
   - It must handle `HTTP POST` requests to the endpoint `/apply`.
   - It must require an `Authorization` header containing exactly: `Bearer k8s-operator-token-123`. If the header is missing or incorrect, return HTTP 401 Unauthorized.
   - The body of the POST request will be a standard-looking Kubernetes YAML manifest (containing at least `metadata.name` and `spec.replicas`).

2. **Integrate the Compiler**:
   When the operator receives a valid POST request, it should:
   - Save the request body to a temporary file.
   - Execute `/app/manifest_compiler <path_to_temp_file>`.
   - If the compiler exits successfully (exit code 0), return an `HTTP 200 OK` with the exact stdout of the compiler as the HTTP response body.
   - If the compiler fails (exit code != 0), return an `HTTP 400 Bad Request` with the stdout/stderr as the response body.
   - If successful, save the original YAML payload to `/home/user/manifests/<name>.yaml` (extracting the `<name>` from the compiler's output or the YAML itself).

3. **Backup Strategy and Automation**:
   - Create a shell script `/home/user/backup.sh` that creates a compressed tarball of the `/home/user/manifests/` directory and saves it to `/home/user/backups/backup_$(date +%s).tar.gz`.
   - Ensure it keeps only the 3 most recent backups in the `/home/user/backups/` directory, deleting older ones.
   - Create a scheduler script `/home/user/scheduler.sh` that runs `backup.sh` every 2 seconds in an infinite loop. 
   
Start the compiled C server and the `scheduler.sh` in the background before declaring the task complete. Ensure the `manifests` and `backups` directories exist.
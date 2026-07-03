You are an AI assistant tasked with building a secure configuration manager in Go. 

As a configuration manager, our system receives periodic backup archives from various environments. Unfortunately, we suspect that some archives might be maliciously constructed to overwrite system files when extracted—a vulnerability known as "Zip Slip" or "Tar Slip". 

Your task is to write and execute a Go program that processes a nested configuration backup, securely extracts it, and merges the valid configurations into a unified format, while strictly logging any security violations.

Here are your specific requirements:

1. **Input:** You will find an uncompressed tar archive at `/home/user/incoming/backups.tar`. This archive contains several nested archives (these can be `.zip` or `.tar.gz` files).
2. **Secure Extraction & Nested Archive Handling:** 
   Your Go program must extract the contents of `backups.tar` and then iterate through any nested `.zip` or `.tar.gz` files inside it, extracting their contents in memory or to a safe temporary directory. 
   **Security Constraint:** As you inspect the files inside the nested archives, you must check their target paths. Any file whose extracted path would escape the extraction directory (e.g., paths starting with `/`, containing `../`, or `..\`) MUST NOT be extracted. 
3. **Security Logging:** For every malicious file path detected in step 2, write the exact raw path string (from the archive header) to a log file at `/home/user/output/security_alerts.log`. Write one path per line, sorted alphabetically.
4. **Configuration Parsing & Merging:**
   The valid files safely extracted from the archives are JSON configuration files. Each valid JSON file has the following structure:
   ```json
   {
     "service": "service_name",
     "version": "1.x",
     "settings": { ... }
   }
   ```
   Parse all securely extracted JSON files. Merge them into a single JSON array containing all the configuration objects.
5. **Output Writing:**
   Sort the merged JSON array alphabetically by the `service` string.
   Write the final formatted JSON array to `/home/user/output/merged_configs.json` using standard JSON indentation (2 spaces).

Directories:
- `/home/user/incoming` (Contains the input files, read-only intent but you can read it)
- `/home/user/output` (You must create this directory and place your outputs here)

Write the Go program (e.g., `/home/user/processor.go`), compile it, and run it to produce the final outputs.
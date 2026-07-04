You are a backup operator testing a new disaster recovery pipeline. We have a partial system state that needs to be fully restored and validated. 

Your tasks involve configuring a web server, sending an email alert, and optimizing a C-based restore tool.

1. **Web Server Setup**: 
   We have an Nginx instance running. Its configuration file is located at `/home/user/nginx/nginx.conf`. You must modify it so that Nginx serves files from `/home/user/restore_out` on port 8080. Reload or restart the Nginx service (running under the user account, not as root).

2. **Email Alert Configuration**:
   A local SMTP server mock is running on `127.0.0.1:2525`. Ensure your C tool (described below) sends a simple email to `backup-admin@local` with the subject "Restore Complete" when the restore finishes successfully.

3. **Restore Tool Implementation and Optimization (C)**:
   In `/home/user/src/restore_tool.c`, there is a skeleton C program designed to parse a proprietary backup format. 
   The backup file `/home/user/data/backup.dat` consists of multiple chunks. Each chunk has:
   - A 4-byte integer (little-endian) specifying the chunk data length (`L`).
   - `L` bytes of actual file data.
   
   Your task is to write the C code to read this file, extract the raw data (ignoring the length headers), and append it to `/home/user/restore_out/recovered.bin`. 
   After writing the file, the tool must connect to the local SMTP server at `127.0.0.1:2525` and send the success email.
   
   **Performance Requirement**: The restore operation must be highly efficient. You must optimize your C code (e.g., using buffered I/O, optimal chunk sizes, or `mmap`) so that it processes the 50MB backup file in under 0.2 seconds. Compile your tool to `/home/user/bin/restore_tool`.

To test your workflow, run your compiled tool. Ensure that Nginx serves the file correctly at `http://127.0.0.1:8080/recovered.bin`.
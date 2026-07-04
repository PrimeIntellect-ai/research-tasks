You are a storage administrator managing disk space on a critical Linux server. We have a large log archive located at `/home/user/system_logs.tar.gz` that contains various server logs.

Your task is to perform the following operations:
1. Verify the integrity of the gzip archive `/home/user/system_logs.tar.gz` to ensure it is not corrupted. 
2. Write a C program named `/home/user/filter_logs.c` and compile it to `/home/user/filter_logs`. This program must act as a stream filter (reading from standard input and writing to standard output). It needs to perform two large-scale text editing operations on the incoming text:
   - Drop (do not print) any line that begins exactly with the string `[TRACE]`
   - Replace any occurrence of the exact string `ERROR_CODE:999` with `ERROR_CODE:000` (assume this string only appears once per line if it does).
3. Without extracting the file to the disk first, use standard stream redirection and piping to extract the contents of `server_01.log` from the archive, pipe it through your compiled `/home/user/filter_logs` program, and save the final output to `/home/user/cleaned_server_01.log`.

Ensure your C program is robust enough to handle standard line lengths (up to 1024 characters). Do not modify the original archive.
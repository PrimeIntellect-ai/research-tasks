Wake up, you're on-call. It's 3:00 AM and we just received a critical page: the primary authentication service (`authd`) segfaulted, and an automated cleanup script accidentally wiped the directory containing the audit logs. We need to piece together the events leading to the crash, recover the lost data, and fix the internal query tool used to analyze these logs.

Here is your incident response plan:

1. **Fix the Vendored Query Tool:** 
   Our custom log analysis tool is vendored at `/app/log-query-1.0/`. However, the previous engineer committed a broken `Makefile` (it fails to link a necessary library and has a misconfigured environment variable `DATA_DIR`). Diagnose the build errors, fix the `Makefile`, and compile the binary to `/app/log-query-1.0/log-query`.

2. **Memory Dump Analysis:**
   The process core dump from the crash is located at `/app/authd.core`. Before it crashed, `authd` loaded a temporary decryption key into memory. Extract this key (it is a 32-character string prefixed with `AUTHKEY-`) and save it to `/app/extracted_key.txt`.

3. **Deleted File Recovery & Optimization:**
   We have a raw disk image of the logs partition at `/app/logs_partition.img`. We started writing a C tool at `/app/recover_logs.c` to carve out the deleted log entries (which start with the magic bytes `[AUDIT]` and end with a newline) from the raw image. 
   However, the current implementation is broken (it misses entries that cross block boundaries) and is extremely slow ($O(N^2)$ string concatenation memory leak). 
   Fix the C code in `/app/recover_logs.c` so that it correctly recovers all `[AUDIT]` log lines. Furthermore, you must optimize it. The tool must accept the disk image path as the first argument and the output file path as the second argument:
   `./recover_logs /app/logs_partition.img /app/recovered.log`

4. **Timeline Reconstruction:**
   Use the compiled `/app/log-query-1.0/log-query` tool along with your recovered `/app/recovered.log` to generate the final event timeline. The query tool requires the `AUTH_KEY` environment variable to be set to the key you extracted in Step 2.
   Run: `AUTH_KEY=$(cat /app/extracted_key.txt) /app/log-query-1.0/log-query parse /app/recovered.log > /app/final_timeline.txt`

**Constraints & Verification:**
- You must use C for fixing `/app/recover_logs.c`.
- An automated verifier will test your compiled `/app/recover_logs` binary on a held-out, 500MB raw disk image to evaluate its correctness and performance. Your binary must recover the logs exactly and execute in under **1.0 seconds** (metric threshold).
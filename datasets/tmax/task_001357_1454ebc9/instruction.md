You are a backup administrator tasked with archiving data logs from multiple legacy servers. The system relies on a custom binary backup format. We are migrating to a new storage backend, and you need to build a filtering proxy to sanitize these backups in transit.

Your task has two phases:

**Phase 1: Write a C Filter Program**
Write a C program at `/home/user/bup_filter.c` and compile it to `/home/user/bup_filter`. This program must read a custom binary archive format from `stdin` and output the sanitized payload to `stdout`.

The input format is strictly defined as:
1. **Magic Header:** 4 bytes, exactly `BKA\x01`. 
   - If this does not match, output `ERR: BAD_MAGIC\n` to `stderr` and exit with status `1`.
2. **Payload Length:** 4 bytes, an unsigned 32-bit integer (little-endian), representing `L`.
3. **Payload:** Exactly `L` bytes of data.
   - If `stdin` reaches EOF before `L` bytes are read, output `ERR: TRUNCATED\n` to `stderr` and exit with status `2`.
4. **Checksum:** 4 bytes, an unsigned 32-bit integer (little-endian). 
   - The checksum is the simple arithmetic sum of all `L` payload bytes (modulo 2^32).
   - If the checksum does not match, output `ERR: BAD_CSUM\n` to `stderr` and exit with status `3`.

If the archive is perfectly valid, you must sanitize the payload. The payload consists of ASCII text lines separated by the newline character `\n`. You must print every line to `stdout` *unless* the line begins exactly with the string `SECRET:`. Lines starting with `SECRET:` must be completely omitted (including their trailing newline) from the output.

**Phase 2: Service Composition**
We have two existing services running on this machine that you need to connect:
- **Backup Sender:** A service repeatedly attempting to send `.bka` streams via TCP to `localhost:7070`.
- **Storage Backend:** A service listening on `localhost:9090` that expects sanitized, plain-text logs over TCP.

You must glue these services together. Create a bash script at `/home/user/start_proxy.sh` that starts a background process (using tools like `socat`, `nc`, etc.) which listens on TCP port `7070`, pipes all incoming data through your `/home/user/bup_filter` executable, and forwards the output to TCP port `9090`. 

Make sure your script is executable (`chmod +x`). Start the script so the proxy is running and the sender successfully transmits its data to the storage backend.
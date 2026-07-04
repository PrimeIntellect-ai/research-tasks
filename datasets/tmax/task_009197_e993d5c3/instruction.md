You are a DevSecOps engineer responsible for enforcing policy-as-code for a critical internal service. We have a legacy C-based file upload daemon located at `/home/user/upload_server.c`. It listens on TCP port 9000 and receives files from internal clients. 

Security audits have revealed three critical flaws in the current implementation:
1. **Path Traversal:** The server blindly trusts the filename provided by the client, allowing an attacker to write files outside the intended `/home/user/uploads/` directory.
2. **Missing Integrity Checks:** The client protocol sends a SHA-256 hash of the file along with the payload, but the server currently ignores it, risking the storage of corrupted or tampered files.
3. **Lack of Sandboxing:** The daemon runs without any syscall restrictions, meaning a theoretical buffer overflow could easily lead to remote code execution (RCE).

Your task is to fix `/home/user/upload_server.c` by implementing the following security controls:

**1. Input Validation (Path Traversal Fix):**
Sanitize the incoming filename. You must reject any filename that:
- Contains the substring `..`
- Contains a forward slash `/`
- Contains any characters other than alphanumeric characters, underscores (`_`), and a single dot (`.`).
If a filename is rejected, write exactly `REJECTED: Path traversal attempt: <filename>` to `/home/user/server.log` and close the connection without writing the file.

**2. Cryptographic Hash Verification:**
The custom protocol format received from the client over the socket is exactly:
- `[64 bytes]`: Expected SHA-256 hash in lowercase hex characters.
- `[256 bytes]`: Null-padded filename.
- `[Remaining bytes]`: File content payload until the connection closes.

You must hash the "File content payload" using OpenSSL (`libcrypto`) SHA-256. If the computed hash does not perfectly match the 64-byte expected hash provided in the header, write exactly `REJECTED: Hash mismatch for <filename>` to `/home/user/server.log` and do not save the file. 

**3. Process Isolation (Seccomp Sandboxing):**
Enforce policy-as-code by adding strict seccomp-bpf filtering using `libseccomp`. Before the server starts accepting connections, it must apply a filter that blocks the `execve` and `execveat` system calls to prevent RCE. The default action for the seccomp filter should be ALLOW (so standard network and file I/O operations continue to work), but `execve` and `execveat` must be set to KILL_PROCESS.

**4. Successful Upload Handling:**
If the filename is valid and the hash matches, save the file to `/home/user/uploads/<filename>` and append exactly `ACCEPTED: <filename>` to `/home/user/server.log`.

**Constraints & Setup:**
- You must compile your fixed code to `/home/user/upload_server`. You can assume `libssl-dev` and `libseccomp-dev` are installed. Use `gcc /home/user/upload_server.c -o /home/user/upload_server -lcrypto -lseccomp`.
- The uploads directory `/home/user/uploads` exists.
- Do not change the listening port (9000). 
- Run your server in the background once compiled.
- Create `/home/user/server.log` before starting your server.
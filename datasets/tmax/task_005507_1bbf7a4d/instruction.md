You are a network engineer analyzing suspicious traffic directed at a legacy web application's file upload endpoint. You suspect the attacker is attempting a path traversal attack.

You have been provided with two files in your home directory (`/home/user/`):
1. `payloads.txt`: A text file containing a list of hex-encoded payloads extracted from the network traffic.
2. `encoder`: A stripped Linux executable that the attacker uses to encode their file paths. 

Your objectives are:

1. **Reverse Engineering:** Analyze the `/home/user/encoder` binary to understand how it transforms plaintext paths into the hex strings found in `payloads.txt`. You may interact with the binary by providing it input or by inspecting it with standard Linux utilities.
2. **Payload Decoding & Sandboxing (Rust):** Write a Rust program in `/home/user/analyzer/` that:
   - Reads the payloads from `/home/user/payloads.txt`.
   - Decodes each payload back to its original plaintext string based on the logic you reverse-engineered.
   - Treats the decoded string as a relative path appended to a simulated sandbox directory: `/var/www/uploads/`.
   - Resolves the path to its shortest absolute form (e.g., resolving `..` and `.`) to determine if the resulting path "escapes" the `/var/www/uploads/` directory boundary. You must compute the logical path (do not rely on the file actually existing on the disk, as these are simulated attacks).
3. **Logging:** For every payload that successfully escapes the sandbox directory (i.e., the resolved path does not start with `/var/www/uploads`), append a line to `/home/user/escapes.log` in the exact following format:
   `[Original Hex] -> [Decoded Plaintext Path] -> [Resolved Absolute Path]`

Example line in `/home/user/escapes.log`:
`747475616263 -> ../abc -> /var/www/abc`

Rules:
- You must write the analyzer in Rust.
- Only log the payloads that escape the sandbox.
- Assume the base sandbox directory is strictly `/var/www/uploads`. No trailing slash in the final resolved path unless it is the root directory `/`.
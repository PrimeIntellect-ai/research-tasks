As a compliance analyst, you are tasked with generating secure audit tokens for our latest SSH access and privilege escalation review. We need to process audit records that contain a user's SSH key fingerprint and their sudo escalation privileges, outputting a base64-encoded validation token.

To do this, you must use a C program that links against `libb64`, a standard Base64 encoding library. 

Here are your instructions:

1. **Fix the Vendored Library:**
   We have vendored the source code for `libb64-1.2.1` in `/app/libb64-1.2.1`. However, a junior analyst recently modified `/app/libb64-1.2.1/src/Makefile` and accidentally broke the build syntax. 
   - Identify and fix the perturbation in the `src/Makefile`.
   - Run `make` in `/app/libb64-1.2.1` to build the static library (`libb64.a`) and ensure the object files compile successfully.

2. **Develop the Audit Token Generator:**
   Write a C program at `/home/user/audit_token_gen.c` that does the following:
   - Reads exactly one line from standard input (stdin) containing up to 256 characters.
   - The input will be in the format: `USERNAME,SSH_KEY_FINGERPRINT,HAS_SUDO` 
     (e.g., `alice,SHA256:abcd1234abcd1234abcd1234abcd1234abcd1234abc,1`).
   - Parses the `USERNAME` and `HAS_SUDO` (which will be `0` or `1`) fields.
   - Constructs a structured audit string exactly formatted as: `AUDIT_TOKEN:user=[USERNAME]:sudo=[HAS_SUDO]`
   - Uses the fixed `libb64` library (`#include <b64/cencode.h>`) to Base64-encode the constructed audit string. Make sure to initialize the encoder state, encode the block, and encode the end of the data.
   - Prints ONLY the resulting Base64-encoded string to standard output (stdout), ending with a single newline (which the b64 library encoder typically adds, just ensure exactly one trailing newline).

3. **Compile the Generator:**
   Compile your program into an executable at `/home/user/audit_token_gen`. Ensure it links against the built `libb64.a` and includes the correct headers from the `/app/libb64-1.2.1/include` directory.

Your final executable must be extremely robust and will be heavily tested against an oracle with hundreds of generated audit logs.
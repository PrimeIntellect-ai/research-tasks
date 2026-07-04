You are a DevSecOps engineer enforcing policy as code. We have a legacy access system that passes restricted SSH commands via weakly encrypted HTTP cookies. Your task is to fix our vendored extraction tool and create a robust script that processes these cookies into hardened SSH `authorized_keys` entries.

1. **Fix the Vendored Package**: We have a vendored package at `/app/cookie-extractor-1.0`. It is a simple tool meant to parse the `CommandToken` from an HTTP Cookie header. However, it currently fails to build using `make`. You must identify the perturbation (a misconfigured source file name in the Makefile) and fix it so that running `make` successfully produces the executable `/app/cookie-extractor-1.0/cookie-extractor`.

2. **Implement the Processing Script**: Create an executable script at `/home/user/generate_auth.sh` that does the following:
   - Reads a single line from STDIN representing an HTTP Cookie header (e.g., `Cookie: session=123; CommandToken=4d3f2c; user=admin`).
   - Uses `/app/cookie-extractor-1.0/cookie-extractor` to extract the `CommandToken` hex string.
   - The `CommandToken` has been obfuscated using a single-byte XOR cipher with the key `0x5A`. Perform cryptanalysis/decryption on this hex string to recover the plaintext ASCII command.
   - Output exactly one line to STDOUT representing a hardened SSH `authorized_keys` entry. It must use the decrypted command in the `command="..."` option, along with the `restrict` option. Use the following static SSH key for the output:
     `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEx1234567890abcdefghijklmnopqrstuvwxyz123 dummy@key`

   Example output format:
   `restrict,command="whoami" ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEx1234567890abcdefghijklmnopqrstuvwxyz123 dummy@key`

Your script must be deterministic and will be tested against 100 randomly fuzzed valid HTTP cookies to ensure bit-exact equivalence with our reference implementation. Ensure your script gracefully handles varying cookie orders and contents, as long as `CommandToken` is present.
You are a build engineer managing dependency artifacts for a web project. We use a proprietary, stripped binary tool located at `/app/deps_compiler` to compile cross-language bindings (Rust/C FFI) into web assembly assets. 

Recently, we discovered that `deps_compiler` is vulnerable to path traversal, shell injection, and memory corruption (due to unsafe FFI constraints) if fed maliciously crafted or out-of-state dependency descriptor files. We cannot patch the binary right now.

Your task is to write a strict validation wrapper in Bash, located at `/home/user/safeguard.sh`. 

The wrapper must accept a single argument (the path to a descriptor file) and implement a strict state machine parser to validate the contents before it would be passed to the compiler. 

The descriptor file must strictly adhere to the following grammar and constraints:
1. The first line MUST be exactly `BEGIN_ARTIFACT`.
2. Following that, there MUST be one or more dependency lines of the format: `DEP <pkg_name> <version>`. 
   - `<pkg_name>` and `<version>` must consist ONLY of alphanumeric characters, hyphens, and dots (no spaces, no special shell characters, no HTML tags).
3. Following the dependencies, there MUST be exactly one FFI binding line: `FFI_BIND <header_path>`.
   - `<header_path>` must be an absolute Unix path starting with `/`.
   - It can only contain alphanumeric characters, slashes, hyphens, and dots.
   - It MUST NOT contain any path traversal components (`..`).
4. The final line MUST be exactly `END_ARTIFACT`.
5. No extra lines, missing lines, or out-of-order lines are allowed.

If the file strictly conforms to this state machine and all constraints, your script must output exactly `ACCEPT` to standard output and exit with code 0.
If the file violates ANY of the format rules, contains invalid characters, or exhibits path traversal attempts, your script must output exactly `REJECT` to standard output and exit with code 1.

To help you develop this, we have provided two directories of test cases:
- `/home/user/corpus/clean/`: Contains 10 valid descriptor files.
- `/home/user/corpus/evil/`: Contains 10 adversarial files that attempt path traversal, XSS via package names, shell injections, or state machine violations.

You can also test the stripped binary `/app/deps_compiler` against these files using reverse engineering tools (like `objdump` or `strings`) if you wish to understand the crashes, but your primary deliverable is the `/home/user/safeguard.sh` script.

Make sure `/home/user/safeguard.sh` is executable.
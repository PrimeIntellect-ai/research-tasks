You are a penetration tester attempting to reverse-engineer a custom malware dropper. The dropper uses a specific payload encoding mechanism and relies on mutual TLS for communication. 

Your objective is to fix a corrupted dependency, generate the necessary certificates, and write a Rust program that perfectly mimics the dropper's payload decoding algorithm.

**Stage 1: Fix the Dependency**
We have vendored the source code of the Rust `goblin` crate (version 0.7.1) at `/app/goblin-0.7.1`. The target malware heavily relies on this for ELF parsing. However, the vendored source has a deliberate perturbation that prevents it from compiling. Identify and fix the build issue in the `Cargo.toml` or source files so that `cargo build` succeeds inside `/app/goblin-0.7.1`.

**Stage 2: Generate TLS Certificates**
The dropper expects client certificates with strict permissions to authenticate to its Command & Control server.
1. Create a directory `/home/user/certs`.
2. Generate a self-signed RSA 2048-bit certificate and unencrypted private key.
3. Save the certificate to `/home/user/certs/client.crt` and the key to `/home/user/certs/client.key`.
4. The private key MUST have strictly `0400` file permissions. 

**Stage 3: Implement the Payload Decoder**
You must write a Rust command-line application in `/home/user/solution`.
1. The project must depend on your fixed local version of `goblin` at `/app/goblin-0.7.1`.
2. The executable must be compiled in release mode, resulting in the binary: `/home/user/solution/target/release/decoder`.
3. **Behavior:**
   - The program reads exactly one line of text from Standard Input (stdin).
   - It decodes the text as Standard Base64.
   - It performs a bitwise XOR operation on every decoded byte using the static key `0x5A`.
   - It checks the first 4 bytes of the resulting data. If they match the standard ELF magic number (`0x7F`, `0x45`, `0x4C`, `0x46`), it writes the raw, decoded (XORed) byte array directly to Standard Output (stdout) and exits with code 0.
   - If the Base64 is invalid, or if the decoded data is less than 4 bytes, or if the magic number does not match, the program must print exactly `INVALID_ELF` (without quotes, followed by a newline) to stdout and exit with code 1.

Your decoder will be rigorously fuzzed against a ground-truth oracle binary extracted from the malware to ensure 100% bit-exact equivalence in behavior.
You are an integration developer tasked with building a hybrid C/Rust gRPC malware scanner for proprietary `.pld` payload files. These files contain a custom header and an x86_64 executable code section.

Your task consists of three phases:

**1. Fix the Vendored C Parser**
We have vendored a minimal C library under `/app/libpld/` that parses `.pld` files. Its `Makefile` has a critical flaw in how it produces the static library archive `libpld.a`, causing linking to fail in Rust. 
- Fix the `Makefile` in `/app/libpld/` so that running `make` correctly builds a standard static archive `libpld.a`.
- The library exposes this API (defined in `/app/libpld/pld.h`):
  ```c
  #include <stdint.h>
  #include <stddef.h>

  struct Pld {
      const uint8_t* code;
      size_t len;
  };
  
  // Parses raw file bytes. Returns NULL on invalid format.
  struct Pld* parse_pld(const uint8_t* data, size_t data_len);
  void free_pld(struct Pld* pld);
  ```

**2. Create a Rust gRPC Service**
Initialize a new Rust project in `/home/user/scanner`. 
- Define a protobuf service `Scanner` with an RPC `CheckPayload` that takes a request containing raw file bytes (`bytes payload = 1;`) and returns a response containing a boolean (`bool is_safe = 1;`).
- Implement the server in Rust (e.g., using `tonic`). It must bind to `127.0.0.1:50051`.
- Use a `build.rs` script to compile your protobuf and statically link the fixed `libpld.a`.
- **Detection Logic:** In your gRPC endpoint, pass the request bytes to `parse_pld`. Analyze the extracted `code` buffer (which contains x86_64 machine code). To prevent malicious execution, you must mark the payload as unsafe (`is_safe = false`) if it contains ANY of the following x86 system call instructions:
  - `syscall` (Opcode: `0x0F 0x05`)
  - `int 0x80` (Opcode: `0xCD 0x80`)
  If the payload does not contain these byte sequences, it is safe (`is_safe = true`). If `parse_pld` returns NULL, treat it as safe.

**3. Build the CLI Verifier Client**
In the same Rust project, create a client binary `scanner-cli` (e.g., in `src/bin/client.rs`).
- It must take exactly two CLI arguments: the server address (e.g., `http://127.0.0.1:50051`) and the path to a `.pld` file.
- It must read the file, send it via gRPC to the server, and print EXACTLY the string `EVIL` to standard output if `is_safe` is false, or `SAFE` if `is_safe` is true. Do not print anything else to stdout.

**Submission Requirements**
Once finished, compile your project and start your gRPC server in the background. Leave the server running on `127.0.0.1:50051`. The automated test suite will invoke your `scanner-cli` binary against a secret directory of benign and malicious payloads to verify your integration and detection logic.
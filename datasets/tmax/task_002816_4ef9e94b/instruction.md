Hello! We have a critical system administration task regarding our backup infrastructure. Our team uses a custom token validation helper for our secure backup server. Unfortunately, the original source code for this utility was lost during a recent storage failure. We only have a compiled stripped version of it at `/app/oracle_validator` and a system architecture diagram located at `/app/arch.png`.

Your task is to reverse-engineer and rewrite this utility in Rust so we can integrate it back into our CI/CD pipelines.

Here is what we know about the validation logic:
1. The program accepts exactly one command-line argument: the token string.
2. It concatenates the token string with a secret `SALT`.
3. It computes the MD5 hash of the resulting string.
4. It checks if the hexadecimal representation of the hash starts with a specific `PREFIX`.
5. If it does, it prints `VALID` to standard output. Otherwise, or if the wrong number of arguments is provided, it prints `INVALID`.

The secret `SALT` and the `PREFIX` are documented within the text of the architecture diagram image at `/app/arch.png`. You will need to extract them (for example, using OCR tools like `tesseract` which is installed on the system).

Please do the following:
1. Initialize a new Rust project at `/home/user/validator`.
2. Add any necessary dependencies (like `md5`) to your `Cargo.toml`.
3. Write the Rust implementation in `/home/user/validator/src/main.rs`.
4. Build the project in release mode so the final executable is located at `/home/user/validator/target/release/validator`.

An automated verifier will test your compiled executable against the `oracle_validator`. It will fuzz both binaries with thousands of random alphanumeric tokens to ensure their outputs are strictly bit-for-bit equivalent.
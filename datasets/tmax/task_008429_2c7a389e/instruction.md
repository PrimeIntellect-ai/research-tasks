You are tasked with fixing a broken Go web security utility that wraps a C shared library. 

The project is located in `/home/user/crypto-wrapper`. It contains:
- `libcrypto.so`: A compiled C shared library.
- `crypto.h`: The header file for the shared library, providing checksum (CRC32) and character encoding (ROT13) routines.
- `main.go`: The Go application using `cgo` to interface with the shared library. It uses a custom data structure `SecurePayload` to manage the processed data.

Currently, `main.go` fails to build. 

Your objectives are:
1. Fix `main.go` so it compiles successfully. The code is missing the proper `cgo` linking directives to link against `libcrypto.so` in the current directory.
2. Create an end-to-end orchestration shell script at `/home/user/test.sh`. The script should:
   - Build the Go application into an executable named `wrapper` in the `/home/user/crypto-wrapper` directory.
   - Execute the `wrapper` binary with the argument `"HelloWebSecurity"`. Make sure the dynamic linker can find `libcrypto.so` at runtime.
   - Capture the standard output of the executable (which is in the format `encoded_string:checksum`), Base64 encode it, and save the base64 string to `/home/user/final.txt`.

Ensure your `test.sh` has executable permissions and works reliably when run.
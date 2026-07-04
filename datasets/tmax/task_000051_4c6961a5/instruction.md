I am porting a legacy C-based web security token validation tool to a Go-based service for deployment in a minimal container. The legacy tool uses a custom polynomial hashing algorithm (acting as a checksum) to validate signed session tokens. 

I have started the Go port in `/home/user/websec_port`, but I'm running into a few issues:
1. I have a `Makefile` that builds a static C library (`libpolyhash.a`), but my Go code is failing to link against it.
2. I need the Go code to process a large file of tokens concurrently, as doing it sequentially is too slow for our requirements.

Your task is to fix the project and run the validation:
1. Fix the Go code in `/home/user/websec_port/main.go` so it properly links to the C library. You may need to build the C library first using the provided `Makefile`.
2. Implement a concurrent worker pool in `main.go` using goroutines and channels to read tokens from `/home/user/websec_port/tokens.txt`.
3. The Go program must pass each token to the C function `unsigned int validate_token(const char* token)`. A token is valid if this function returns `1`.
4. The Go program must write all valid tokens to `/home/user/websec_port/valid_tokens.txt`, with one token per line. The order of tokens in the output file does not matter.

To complete the task:
- Ensure `main.go` compiles successfully with `go build`.
- Run the compiled binary to process `tokens.txt`.
- Ensure `/home/user/websec_port/valid_tokens.txt` is created with the correct valid tokens.
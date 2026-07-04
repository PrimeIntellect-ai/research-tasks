You need to fix and complete a high-performance URL routing application in Rust. We recently received a security module update, but the developer left it in a broken state. 

Your objectives are to extract the latest code patch, fix the resulting compilation errors (which heavily involve Rust lifetimes), implement a validation function from an assembly reference, and ensure your compiled binary exactly matches our strict security oracle.

**Step 1: Extract and Apply the Patch**
There is a security feed video located at `/app/security_feed.mp4`. The previous developer embedded a base64-encoded `.patch` file inside the video's `title` metadata field (you can use `ffprobe` to inspect it). 
1. Extract the base64 string from the `title` metadata.
2. Decode it into a file and apply the patch to the Rust project located at `/home/user/secure_router`. 
This patch introduces a performance benchmarking suite and updates our URL routing parameters to use zero-copy parsing.

**Step 2: Fix the Lifetime Errors**
The patch significantly breaks the build. The developer tried to make the `Router` and `Route` structs zero-copy by having them hold string slices (`&str`) instead of owned `String`s, but the lifetime annotations in `src/parser.rs` and `src/main.rs` are completely broken.
1. Fix the compile errors by correctly annotating the lifetimes so that the parsed routing segments and query parameters properly borrow from the input URL string.
2. Do not change the fundamental architecture to use `String`; it must remain zero-copy (`&str`) for performance benchmarking reasons.

**Step 3: Implement the Assembly Validator**
Inside `src/validator.rs`, there is a placeholder function `pub fn validate_token(token: &str) -> bool`. 
We lost the original C source code for the proprietary token validation logic. You must reverse-engineer the x86_64 assembly provided in `/home/user/secure_router/asm/validator_x64.asm` and implement its exact logic in pure Rust inside `validate_token`. The assembly takes a string pointer and length, validates boundaries, and computes a specific rolling checksum with bitwise operations.

**Step 4: Build and Verify**
Build the project using `cargo build --release`. 
The resulting binary will be located at `/home/user/secure_router/target/release/url_processor`. 
This executable takes a single URL as a CLI argument. 
Example usage: `/home/user/secure_router/target/release/url_processor "/api/v1/data?token=abcdef&user=admin"`

The binary must output precisely one line to STDOUT:
- If the token is invalid according to your ASM implementation: `REJECT: Invalid Token`
- If the token is valid, it prints the extracted routing path: `ACCEPT: <normalized_path>`

Ensure your binary is functionally flawless. It will be verified against an aggressive fuzzer comparing your implementation's output to a closed-source reference oracle for thousands of URL variations.
You are an engineer tasked with porting a minimal Linux hardware-profiling tool into a containerized environment. The tool is written in Rust.

Currently, the project is located at `/home/user/min_tool`. The build is broken due to a package version mismatch, and the core hardware profiling function is missing its assembly implementation.

Your tasks are to:
1. **Dependency & Semver Fix**: The project requires the `semver` crate. The code in `src/main.rs` is written for `semver` version `1.0.0` or higher (using the `VersionReq::parse` and `matches` API). However, `Cargo.toml` has a broken or outdated dependency constraint. Update `/home/user/min_tool/Cargo.toml` so it uses `semver = "1.0"`.
2. **Assembly-level Construction**: In `/home/user/min_tool/src/main.rs`, there is a function `fn cpuid_vendor() -> [u8; 12]`. It currently returns an array of zeros. You must implement this using Rust's x86_64 inline assembly (`core::arch::asm!`). You need to call the `cpuid` instruction with `eax = 0`. The CPU vendor string (12 bytes) is returned in the `ebx`, `edx`, and `ecx` registers (in that order). Construct the 12-byte array from these registers and return it.
3. **Benchmarking & Execution**: Once the compilation succeeds and the assembly is correct, run `cargo run --release` inside `/home/user/min_tool`. The program has a built-in benchmarking loop that will evaluate your inline assembly's performance and write a final report to `/home/user/result.json`.

Ensure that the final output file `/home/user/result.json` is successfully generated and contains the correct CPU vendor string (e.g., "GenuineIntel" or "AuthenticAMD").
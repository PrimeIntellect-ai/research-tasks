I'm working on a multi-file Rust project located in `/home/user/router_vm`. It implements a bytecode interpreter (VM) for a custom URL routing language. For performance reasons, the actual string matching logic delegates to a C library via FFI.

However, the project is currently broken:
1. It fails to compile. The build system (`build.rs` and `Cargo.toml`) isn't properly configured to compile and link the C source code located in `c_src/matcher.c`. You need to fix the cross-language build configuration so `cargo build --release` succeeds.
2. Even after you get it to compile, the performance of the VM is terrible. There is a fundamental flaw in the interpreter's main loop in `src/main.rs` that causes a massive bottleneck when processing many URLs. You need to refactor the hot loop to eliminate unnecessary redundant work (hint: look at when and how the routing bytecode is parsed versus executed).

I've provided a reference implementation—a highly optimized, stripped binary at `/app/ref_router_vm`. This binary accepts a bytecode file and a file containing URLs to route.

Your task:
1. Fix the Rust build configuration so the project compiles.
2. Optimize the Rust code in `src/main.rs`. 
3. Build the optimized project using `cargo build --release`. 

When you're finished, leave the optimized, compiled binary at `/home/user/router_vm/target/release/router_vm`. The automated verifier will measure the execution time of your binary against `/app/ref_router_vm` on a large test dataset. Your optimized Rust binary must run at most 1.5x slower than the reference C binary.

Please get my router VM compiling and running quickly!
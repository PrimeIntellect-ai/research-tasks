You are a systems programmer debugging a cross-compilation and linking issue for a Rust project that wraps a C library.

The project is located at `/home/user/accel_lib`. It uses the `cc` crate in its `build.rs` to compile a C library (`src/c/accel.c`) and link it to the Rust code.

Currently, the `build.rs` is hardcoded with incorrect macro definitions, causing compilation and constraint failures when cross-compiling or toggling Cargo features. 

Your task is to fix ``/home/user/accel_lib/build.rs`` to dynamically enforce the following constraint satisfaction rules based on the target architecture (`CARGO_CFG_TARGET_ARCH`) and the `fast_math` Cargo feature (`CARGO_FEATURE_FAST_MATH`):

1. If the target architecture is `x86_64`, define the C macro `MATH_X86=1`.
2. If the target architecture is `aarch64`, define the C macro `MATH_ARM=1`.
3. For any other architecture (e.g., `riscv64`), define `MATH_GENERIC=1`.
4. **Constraint Rule:** The `fast_math` feature relies on hardware-specific assembly. If the `fast_math` feature is enabled AND the architecture resolves to `MATH_GENERIC`, the build script MUST panic with the exact message: `"Constraint violation: fast_math requires x86_64 or aarch64"`.
5. Remove any old, hardcoded macro definitions in `build.rs` that violate these rules.

Once you have fixed `build.rs`:
- Ensure `cargo test` passes on the native host.
- Ensure `cargo check --target riscv64gc-unknown-none-elf` passes.
- Ensure `cargo check --target riscv64gc-unknown-none-elf --features fast_math` fails with your exact panic message.

You do not need to submit any specific output files. Automated tests will verify the correctness of your `build.rs` logic by running the cargo commands mentioned above.
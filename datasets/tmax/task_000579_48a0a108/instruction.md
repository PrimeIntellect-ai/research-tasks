You are a systems programmer working on a hybrid C/Rust project. We have a highly optimized C function for computing the next term in a Hailstone (Collatz) sequence, but the build process is broken, and the Rust wrapper is incomplete. 

Your task is to fix the C library build, complete the Rust FFI bindings, implement a custom data structure, and compute a specific mathematical result.

Here is the setup in `/home/user/hailstone_ffi/`:
1. `/home/user/hailstone_ffi/c_src/fast_math.c` - Contains the optimized C implementation.
2. `/home/user/hailstone_ffi/c_src/fast_math.h` - Contains the signature: `uint64_t next_hailstone(uint64_t n);`
3. `/home/user/hailstone_ffi/c_src/Makefile` - Supposed to build a static library `libfastmath.a`, but it contains a critical error in how it archives the object files.
4. `/home/user/hailstone_ffi/rust_src/` - A Cargo project.

You need to perform the following steps:
1. **Fix the Makefile**: Modify `/home/user/hailstone_ffi/c_src/Makefile` so that `make` correctly builds a valid static library archive `libfastmath.a` using `ar`.
2. **Configure Rust Linking**: Write a `/home/user/hailstone_ffi/rust_src/build.rs` that instructs Cargo to search for and statically link `fastmath` from the `c_src` directory.
3. **Write the Rust FFI and Iterator**: 
   In `/home/user/hailstone_ffi/rust_src/src/lib.rs`, declare the FFI binding to `next_hailstone`.
   Then, design a custom data structure `pub struct HailstoneSeq` that implements the `Iterator` trait over `u64`. 
   - It should be initialized with a starting value `n`.
   - Each call to `next()` should yield the *current* value, and then use the C FFI function to compute the next value.
   - The iterator must terminate (return `None`) *after* it yields the value `1`.
4. **Compute the Target Benchmark**:
   Write `/home/user/hailstone_ffi/rust_src/src/main.rs`. Using your custom iterator, find the **maximum value** reached in the Hailstone sequence starting with `n = 77031`. 
   Write this maximum `u64` value as plain text to `/home/user/result.txt`.

Ensure your Rust code compiles cleanly and outputs the correct mathematical result to the requested file.
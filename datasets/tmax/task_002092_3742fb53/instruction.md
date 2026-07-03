You are tasked with fixing a multi-file Rust project in `/home/user/project` that currently fails to compile because a crucial generated source file is missing. The project relies on a data-driven build process that you must implement.

There are two existing files in the directory:
1. `/home/user/project/main.rs`: The entry point of the Rust program. It expects a module named `magic` containing a constant `MAGIC_NUMBER` of type `u32`.
2. `/home/user/project/ops.txt`: A text file containing custom assembly-like instructions. Each line starts with a semantic version string (X.Y.Z), followed by an operation code, and an integer operand. 

Your objective is to:
1. Parse the `/home/user/project/ops.txt` file using Python.
2. Filter the instructions: ONLY execute instructions where the associated semantic version is strictly greater than or equal to `2.1.0`. Be careful: semantic versions must be compared properly (e.g., `2.10.0` is newer than `2.1.0`, but naive string comparison might fail).
3. Implement a minimal emulator in Python to compute the final state. The emulator has a single 32-bit unsigned integer register initialized to `0`. 
   The valid operations are:
   - `ADD X`: Add X to the register.
   - `SUB X`: Subtract X from the register (wrap around on underflow).
   - `MUL X`: Multiply the register by X.
   - `XOR X`: Bitwise XOR the register with X.
   - `LSHIFT X`: Left shift the register by X bits.
   - `RSHIFT X`: Right shift the register by X bits.
   *Note: All operations should maintain the register as a 32-bit unsigned integer (modulo $2^{32}$).*
4. Generate a Rust file at `/home/user/project/magic.rs` containing the final computed value. The file must exactly contain: `pub const MAGIC_NUMBER: u32 = <final_value>;`
5. Compile the Rust project using the command `rustc main.rs` from within `/home/user/project`.
6. Run the compiled `./main` executable and redirect its standard output to `/home/user/project/output.txt`.

Ensure all generated files are correctly placed in `/home/user/project`. Do not modify `main.rs`.
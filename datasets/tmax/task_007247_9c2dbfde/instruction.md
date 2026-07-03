You are tasked with fixing and completing a Rust-based project file organizer. A developer started building a CLI tool at `/home/user/organizer` that takes a flat list of files and groups them into folders (bins) based on sizes and "conflict" rules (similar to peer dependency conflicts, where certain files cannot exist in the same folder). 

However, the developer struggled with Rust's borrow checker and left the code in a non-compiling state. Furthermore, the constraint validation is untested.

Your objectives:
1. **Fix Ownership/Borrowing Issues:** Fix the compile errors in `/home/user/organizer/src/lib.rs`. The code attempts to implement a greedy bin-packing algorithm with conflicts but has lifetime and mutable borrowing issues. Do not change the function signatures or the core algorithm logic (described below); just fix the Rust-specific errors.
2. **Implement Property-Based Testing:** Add a property-based test in `src/lib.rs` using the `proptest` crate. The test should generate random `FileItem`s and verify that the `organize_files` function *always* returns an allocation where:
   - No bin's total file size exceeds the `max_size`.
   - No bin contains two files that have mutually exclusive tags (as defined by a random set of `ConflictRule`s).
3. **Run the Tool:** Compile the fixed project and run it against the provided JSON input files: `/home/user/input_files.json` and `/home/user/rules.json`. 
   The command is: `cargo run -- /home/user/input_files.json /home/user/rules.json /home/user/allocation.json`

**Algorithm Specification (Greedy Bin Packing with Conflicts):**
To ensure deterministic output, the algorithm (partially written in `lib.rs`) must do the following:
1. Sort the input files descending by `size`. If sizes are equal, sort ascending by `name`.
2. Iterate through the sorted files. For each file, attempt to place it in the *first* (lowest index) existing bin where:
   - Adding the file does not cause the bin's total size to exceed `max_size`.
   - The file does not conflict with any file already in the bin. A conflict occurs if the new file has a tag `A` and an existing file has a tag `B`, and the pair `[A, B]` (or `[B, A]`) exists in the conflict rules.
3. If the file cannot fit in any existing bin, create a new bin at the end of the bin list and place the file there.

Ensure that all tests pass (`cargo test`). The final output must be exactly written to `/home/user/allocation.json` as a JSON array of arrays of file names, representing the bins.
You are tasked with writing a multi-language project organizer that acts as a constraint-satisfaction bin packer and conditional build generator. 

I have a set of source files in `/home/user/raw_files/`. Each file contains a special header on its first line indicating its target architecture, for example: `// ARCH: x86`, `// ARCH: arm`, or `# ARCH: any`.

You need to write a Python script at `/home/user/organizer.py` that organizes these files into numbered directories (`/home/user/organized/bin_1`, `/home/user/organized/bin_2`, etc.) based on the following constraints:
1. **Capacity Constraint**: The total size of files in any single bin must not exceed 100 bytes.
2. **Conflict Constraint**: Files with `ARCH: x86` and `ARCH: arm` CANNOT be placed in the same bin. Files with `ARCH: any` can be placed anywhere, provided the capacity constraint is met.
3. **Bin Minimization**: Use the minimum possible number of bins.
4. **Custom Data Structure**: Implement a `BinTree` or similar custom data structure in your script to manage the bins and validate constraints upon file insertion.

After sorting the files, your script must generate a `build.sh` inside each populated `bin_X` directory. This conditional build script must:
- If the bin contains *any* `x86` file, it should write exactly `gcc -m64 -c *.c` into `build.sh`.
- If the bin contains *any* `arm` file, it should write exactly `aarch64-linux-gnu-gcc -c *.c` into `build.sh`.
- If the bin contains *only* `any` files (e.g., Python scripts), it should write `python3 -m py_compile *.*` into `build.sh`.
- Make the `build.sh` scripts executable.

Finally, write an end-to-end test bash script at `/home/user/test_e2e.sh` that:
1. Clears `/home/user/organized/` (if it exists).
2. Runs your `organizer.py`.
3. Iterates through all created bins and executes their `build.sh` scripts (ignore compile errors, just ensure the scripts run).
4. Outputs the final file-to-bin mapping as a JSON object to `/home/user/allocation.log`, formatted as `{"filename": "bin_X", ...}`.

Please implement `organizer.py` and `test_e2e.sh`, then run `test_e2e.sh` to generate `/home/user/allocation.log`.
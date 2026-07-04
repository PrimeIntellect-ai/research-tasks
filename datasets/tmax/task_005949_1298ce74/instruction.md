You are a systems script developer working on ABI (Application Binary Interface) compatibility utilities. Your team has updated a core C shared library, but several legacy functions were removed, causing dependent applications to crash.

Your task is to analyze the old and new libraries, dynamically generate a minimal assembly "shim" to restore the missing ABI, and produce a unified symbol report.

In the `/home/user/abi_task` directory, you will find two shared libraries (which have already been compiled):
- `libold.so`: The previous version of the library.
- `libnew.so`: The newly updated version of the library.

Perform the following steps:
1. **Analyze and Diff**: Write a script in your language of choice to analyze the exported global text symbols (functions, typically marked 'T' in `nm`) of both libraries. Identify all function symbols that exist in `libold.so` but are completely missing from `libnew.so`. Ignore any symbols that start with an underscore (`_`).
2. **Generate Assembly Shim**: Programmatically generate a minimal x86_64 assembly file at `/home/user/abi_task/shim.s`. For every missing symbol you identified, your assembly file must define a global function with that exact name. Each function must simply return the integer `0` (e.g., clearing the return register and returning). 
3. **Compile the Shim**: Compile `/home/user/abi_task/shim.s` into a shared library named `/home/user/abi_task/libshim.so`.
4. **Merge and Sort Output**: Extract the names of all exported global functions (ignoring those starting with `_`) from both `libnew.so` and your new `libshim.so`. Merge these two lists, sort them alphabetically, and write the resulting deduplicated list to `/home/user/abi_task/final_symbols.txt`, with one symbol name per line.

Constraints:
- You may use any installed tools (`nm`, `readelf`, `objdump`, `gcc`, `python3`, etc.).
- Your assembly must be valid x86_64 and position-independent, suitable for a shared library.
- The final symbol text file must only contain the exact function names, nothing else.
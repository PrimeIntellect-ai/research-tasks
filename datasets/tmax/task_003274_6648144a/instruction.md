You are tasked with creating a lightweight, polyglot build system using only Bash shell scripts and standard Unix tools. You need to write a script that processes dependencies, applies patches, and builds the targets in the correct order.

The working directory is `/home/user/build_system/`.
Inside this directory, you will find:
- `graph.txt`: A file defining the dependencies for each component. Each line is of the format `Target: Dep1 Dep2 ...`.
- `src/`: A directory containing source files (`A.txt`, `B.txt`, `C.txt`, `D.txt`).
- `patches/`: A directory containing patch files. Some components have patches that must be applied to their source files before building.
- `out/`: An initially empty directory where the build outputs should be placed.

You need to create a Bash script at `/home/user/build_system/make.sh`. 
The script must accept a single target name as an argument (e.g., `./make.sh A`).
When executed, your script must perform the following for the requested target and all its transitive dependencies:

1. **Dependency Resolution**: Determine the correct build order. A component must only be built AFTER all of its dependencies have been built.
2. **Patching**: Before a component is built, check if a corresponding `.patch` file exists in the `patches/` directory (e.g., `patches/B.patch` for component `B`). If it does, apply the patch to the component's source file in the `src/` directory. Be careful to apply each patch only once, even if the script is run multiple times. Use the standard `patch` command.
3. **Building**: To "build" a component `X`, create a file named `out/X.out`. The contents of `out/X.out` must be the concatenation of its dependencies' `.out` files (sorted alphabetically by the dependency names), followed by a newline, followed by the component's own (possibly patched) source file contents from `src/X.txt`. If the component has no dependencies, its `.out` file should simply be a copy of its source file. All files concatenated should be separated by newlines if they don't already end in one (ensure standard text file formatting).
4. **Testing**: After the build completes, write the final contents of `out/A.out` to `/home/user/build_system/final_output.log` for verification.

To complete the task:
1. Write the `make.sh` script.
2. Make it executable.
3. Run `./make.sh A` to build target `A` and its dependencies.
4. Ensure `/home/user/build_system/final_output.log` is created and contains the correct build output.
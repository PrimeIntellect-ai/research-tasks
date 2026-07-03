You are tasked with organizing a multi-language project located in `/home/user/project`. This project consists of five micro-packages (a mix of Node.js and Python packages), but the legacy build system has left their dependency manifests in a highly obfuscated state.

The project contains five directories inside `/home/user/project/`, one for each package. Inside each package directory, there is a file named `meta.dat`. 

Each `meta.dat` file contains dependency information that has been encoded twice:
1. First, the plain UTF-8 JSON string was hex-encoded.
2. Then, the resulting hex string was Base64-encoded.

The decoded JSON will have the following structure:
`{"name": "package_name", "deps": ["dependency_name_1", "dependency_name_2"]}`

Your task is to:
1. Read and decode the `meta.dat` files for all packages in `/home/user/project/`.
2. Reconstruct the dependency graph (a Directed Acyclic Graph) for these packages.
3. Compute a valid topological sort to determine the correct build/installation order.
4. **Tie-breaking rule:** If multiple packages are ready to be built at the same time (i.e., they have an in-degree of 0 in the remaining graph), always pick the package whose name comes **first alphabetically**.
5. Output the final, ordered list of package names to `/home/user/build_order.txt`. The format must be a single line of comma-separated package names, with exactly one space after each comma (e.g., `pkgA, pkgB, pkgC`).

Write a script (in Python, Node.js, or Bash) to perform these steps, execute it, and ensure `/home/user/build_order.txt` is created with the correct format.
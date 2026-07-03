You are an open-source maintainer reviewing a broken Pull Request for a package manager prototype. The workspace is located in `/home/user/pkg-mgr`.

The PR introduces a Bash script (`resolve.sh`) that calculates the correct build order from a dependency graph file (`graph.txt`). Because node names can contain spaces and special UTF-8 characters, the graph file encodes all node names in hexadecimal. The PR also includes a fast C utility (`decoder.c`) to decode these hex strings.

However, the PR is currently broken. Your task is to fix the project so that running `./resolve.sh graph.txt` writes the correct build order to `/home/user/build_order.txt`.

**Bugs you need to fix:**
1. **Polyglot Build Interop:** `resolve.sh` attempts to use `./decoder`, but it forgets to compile `decoder.c`. Modify `resolve.sh` to compile `decoder.c` using `gcc -o decoder decoder.c` before doing anything else.
2. **Character/Data Encoding:** The provided `decoder.c` has a bug where it fails to properly parse the hex input into a decoded string (it is missing a length boundary check and might mishandle the string formatting). Fix `decoder.c` so it accurately reads a single hex-encoded string from standard input and prints the decoded raw UTF-8 string followed by a newline.
3. **Graph Resolution:** `resolve.sh` uses `tsort` to generate the build order. However:
   - It constructs the directed edges backwards. For a *build order*, dependencies must be printed *before* the packages that depend on them. 
   - It completely drops packages that have no dependencies (standalone nodes). `tsort` accepts a node paired with itself (e.g., `Node Node`) to declare an isolated vertex. Fix `resolve.sh` to correctly build the edge list and output the final topological sort to `/home/user/build_order.txt`.

**Expected output:**
When finished, running `./resolve.sh graph.txt` must succeed and create `/home/user/build_order.txt` containing the decoded node names, sorted in valid build order (dependencies before dependents), one per line.
I'm developing a set of build utilities to correctly link shared libraries for a complex project, but I've run into two issues that are preventing my toolchain from working. I have a workspace located at `/home/user/utility/`.

First, I have a Rust-based shared library in `/home/user/utility/rust_lib/` that is failing to compile due to a borrow checker error in `src/lib.rs`. I need you to fix the Rust code so it complies with Rust's ownership rules without changing the function signature, and then build the release version of the shared library (`cargo build --release`).

Second, I have a Python script, `/home/user/utility/resolver.py`, which is supposed to parse a custom dependency definition file (`/home/user/utility/deps.txt`), construct a dependency graph, and evaluate the correct link order for the libraries (a topological sort where dependencies must appear *before* the libraries that depend on them). 

Currently, `resolver.py` is incomplete. You need to implement the missing parsing and graph traversal logic in it. 

The dependency file (`deps.txt`) has the following format:
`LibraryName: Dep1 Dep2 Dep3`
If a library has no dependencies, it will just be:
`LibraryName:`

Requirements for `resolver.py`:
1. Parse the constraints from `deps.txt`.
2. Perform a topological sort to resolve the dependencies.
3. If there are multiple valid load orders (e.g., two libraries have their dependencies met simultaneously), break ties by sorting the libraries **alphabetically**.
4. The script must write the final resolved order as a single, comma-separated string (with a space after each comma) to `/home/user/utility/load_order.txt`.

Please fix the Rust library, compile it, and complete the Python script to generate the correct `load_order.txt`.
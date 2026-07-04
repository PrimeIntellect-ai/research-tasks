You are a build engineer managing a set of compiled C plugins for an application. Locally, the test suite passes because the build system inadvertently loads the plugins in the correct order. In CI, however, the tests fail because the plugin load order is non-deterministic, causing symbol dependency and state transformation errors.

You need to write a C-based test fixture to dynamically resolve the dependencies, load the shared libraries in the correct order, and compute a final deterministic verification checksum.

Directory: `/home/user/artifacts`

In this directory, there are 5 compiled shared libraries:
- `libnode.so`
- `libedge.so`
- `libvertex.so`
- `libgraph.so`
- `libtree.so`

Each library exports a single symbol representing its state transformation logic:
`uint32_t process_chunk(uint32_t state);`

Alongside the libraries are 5 plain-text metadata files:
- `node.deps`
- `edge.deps`
- `vertex.deps`
- `graph.deps`
- `tree.deps`

Each `.deps` file contains a newline-separated list of the plugin names (e.g., `node`, `tree`) that the corresponding plugin depends on. If Plugin A depends on Plugin B, Plugin B must be loaded and executed *before* Plugin A.

Your task:
1. Write a C program `/home/user/artifacts/runner.c`.
2. The program must parse the `.deps` files and perform a topological sort to determine the correct execution order. (The dependency graph guarantees a single, unique valid topological sort).
3. The program must use `dlopen` and `dlsym` to dynamically load the libraries in the sorted order.
4. Starting with an initial state of `0x1337`, the program must sequentially pass the state through each plugin's `process_chunk` function (e.g., `state = process_chunk(state);`).
5. The program must write its final results to `/home/user/artifacts/result.log` in exactly this format:
   ```
   Order: <plugin1>, <plugin2>, <plugin3>, <plugin4>, <plugin5>
   Final State: 0x<HEX_STATE_IN_UPPERCASE>
   ```

Compile your runner, execute it, and ensure `result.log` is generated correctly.
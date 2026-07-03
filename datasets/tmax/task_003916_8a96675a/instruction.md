You are a systems programmer debugging a runtime linking issue in a hybrid C/Python mathematical library. The library performs graph traversal operations using adjacency matrix powers.

In `/home/user/mathlib/`, you will find the source code for the library, which consists of a matrix math core (`matrix.c`), a graph algorithms module (`graph.c`), a build script (`build.sh`), and a Python wrapper (`graph_wrapper.py`). 

Currently, the C libraries compile successfully using `./build.sh`, but running `python3 -c "import graph_wrapper"` fails with a linking dependency error: `libgraph.so` cannot find its dependency `libmatrix.so` at runtime. 

Your tasks are:
1. **Fix Dependency Resolution**: Modify `/home/user/mathlib/build.sh` so that `libgraph.so` is built with a hardcoded library path (RPATH) pointing to the absolute path `/home/user/mathlib/lib`. When `./build.sh` is executed, it should produce libraries such that `import graph_wrapper` succeeds immediately without modifying system-wide environment variables like `LD_LIBRARY_PATH`. Run `./build.sh` to apply the fix.
2. **Setup Test Fixtures**: Install `pytest` and `hypothesis` using `pip`.
3. **Property-Based Testing**: Create a test suite in `/home/user/mathlib/test_graph.py`. Use `hypothesis` to test the `get_path_count` function from `graph_wrapper`.
   - Write a property-based test named `test_zero_matrix_paths` that generates a random 4x4 adjacency matrix consisting entirely of `0`s. 
   - Generate a random number of `steps` between `1` and `5`.
   - Generate random `start` and `end` indices between `0` and `3`.
   - Assert that for an empty graph (all zeros), the path count for `steps > 0` is strictly `0`.
   - Write a second property test named `test_zero_steps` that tests any random 4x4 matrix (values 0 or 1), `steps=0`, and random `start`/`end` indices. Assert that the path count is `1` if `start == end`, and `0` otherwise.

Ensure that running `python3 -m pytest /home/user/mathlib/test_graph.py` succeeds with all tests passing.
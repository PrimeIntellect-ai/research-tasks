You are a build engineer managing a Python-based build system. Recently, the Continuous Integration (CI) pipeline has been failing intermittently because our artifact linker loads intermediate build files in an arbitrary filesystem order (dependent on `os.listdir`), which violates dependency constraints and causes the build to fail.

Your task is to write a Python script that resolves the artifact dependencies, enforces a deterministic build order, and merges the numerical data from the artifacts into a final build product.

**Environment and Input Data:**
- The intermediate artifacts are located in the directory `/home/user/artifacts/`.
- There are multiple `.dat` files in this directory. 
- Each file is formatted as follows:
  - Line 1: `DEPENDS: <filename1> <filename2> ...` (A space-separated list of other `.dat` files this artifact depends on. This line might just be `DEPENDS:` if it has no dependencies).
  - Line 2: A space-separated list of exactly 500 integers.

**Your Objectives:**
1. **Dependency Resolution (Graph Traversal):** Parse all `.dat` files in `/home/user/artifacts/` to build a dependency graph. Perform a topological sort to determine the correct build order. An artifact can only be processed *after* all of its dependencies have been processed.
2. **Deterministic Sorting:** To ensure the CI is perfectly reproducible, if multiple artifacts are available to be processed at the same time (i.e., their dependencies are met), you must process them in **alphabetical order** of their filenames.
3. **Artifact Merging (Numerical Algorithm):** 
   - Start with an initial state array of 500 zeros.
   - Iterate through the topologically sorted artifacts.
   - For each artifact, update the state array element-wise using the formula: 
     `state[i] = (state[i] + artifact_data[i]) % 10007`
4. **Outputs:**
   - Create a file `/home/user/build_order.log` containing the exact ordered list of filenames processed, one filename per line.
   - Create a file `/home/user/final_artifact.dat` containing the final 500-element state array, represented as a single line of space-separated integers.

Write your Python script (e.g., `/home/user/linker.py`), execute it, and ensure the two output files are generated precisely as specified.
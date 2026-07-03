You are an engineer setting up a polyglot build system from scratch. As part of this, your team has built a custom dependency resolver in Python that parses a new build file format (`.poly`), extracts semantic version requirements, and generates a build order using a topological sort (graph traversal).

However, the initial prototype script has a few bugs, and we need you to fix it and verify it.

**Context:**
The build system relies on a Python script located at `/home/user/polybuild/build_parser.py`. 
It reads `.poly` files which have the following format (blocks separated by `---`):

```
target: <name>
version: <semantic_version>
depends: <target>@>=<semantic_version>, <target>@>=<semantic_version>
---
```

**Your objectives:**
1. **Fix the Parser & Version Logic:** The current `build_parser.py` script has a bug in how it compares semantic versions (it currently uses naive string comparison, so `1.10.0` is incorrectly evaluated as older than `1.2.0`). Update the `check_version(actual, required)` function to properly compare standard semantic versions (e.g., `MAJOR.MINOR.PATCH`).
2. **Fix the Graph Traversal:** The `get_build_order()` function is supposed to return a valid topological sort of the target names (a list of target names such that every target appears *after* its dependencies). Currently, it has a bug where it fails to properly order independent nodes or handle the root nodes correctly. Fix the graph traversal logic.
3. **Verify via Tests:** Complete the test suite in `/home/user/polybuild/test_parser.py` to cover:
   - Version comparison correctness.
   - Successful parsing of the `/home/user/polybuild/examples/project.poly` file.
   - Correct topological sorting of the project.
4. **Generate Artifacts:** Run your tests using `pytest` and save the standard output to `/home/user/polybuild/test_results.log`. Finally, run the fixed `build_parser.py` on `/home/user/polybuild/examples/project.poly` and redirect its output (which should just be the comma-separated build order) to `/home/user/polybuild/build_order.txt`.

*Note: You must use Python's standard library only for the implementation (no external libraries like `semver` or `networkx`). You may use `pytest` for testing.*
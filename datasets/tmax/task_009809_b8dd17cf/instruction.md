You are helping to migrate a legacy system for dependency resolution. The core solver is written in C++ for performance, and it is wrapped by a Python script. Currently, the system is broken due to a Python 2 to Python 3 migration, and there are underlying logical bugs in the C++ semantic versioning code.

Your objectives:

1. **Fix Python 3 Migration Issues**:
   The wrapper script `/home/user/project/wrapper.py` was written for Python 2. Fix all syntax and standard library issues so it runs correctly in Python 3. The script reads a JSON file of dependencies and passes it to the C++ binary via stdin, then parses the stdout.

2. **Fix C++ Semantic Version Comparison**:
   The C++ solver in `/home/user/project/semver.cpp` has a bug. It compares semantic versions (e.g., "1.2.0" and "1.10.0") lexicographically rather than numerically. Rewrite the `compare_versions(const std::string& a, const std::string& b)` function in `semver.cpp` to correctly parse and compare standard `Major.Minor.Patch` versions. The function should return `-1` if `a < b`, `1` if `a > b`, and `0` if `a == b`.

3. **Implement Property-Based Testing**:
   Write a property-based test using the RapidCheck framework in `/home/user/project/test_semver.cpp`. The test must check at least two properties for your semantic version parser:
   - Symmetry of equality: for any generated version `v`, `compare_versions(v, v) == 0`.
   - Anti-symmetry of comparison: if `compare_versions(a, b) == 1`, then `compare_versions(b, a) == -1`.
   *(Assume RapidCheck is cloned at `/home/user/rapidcheck` and built. You just need to include `<rapidcheck.h>` and link against `librapidcheck.a`)*.

4. **Set Up a CI Script**:
   Create a bash script at `/home/user/project/ci.sh` that:
   - Compiles the main C++ program `solver.cpp`, `semver.cpp`, `graph.cpp` into an executable named `solver`.
   - Compiles and runs the property-based tests `test_semver.cpp` linked with `semver.cpp` and RapidCheck. If the tests fail, the script should exit with a non-zero code.
   - Runs `python3 wrapper.py input.json` and redirects the output to `/home/user/project/output.json`.

**Initial System State**:
- Directory `/home/user/project/` contains `solver.cpp`, `semver.cpp`, `semver.h`, `graph.cpp`, `graph.h`, `wrapper.py`, and `input.json`.
- Directory `/home/user/rapidcheck/` contains the RapidCheck framework (include files in `include/` and compiled `librapidcheck.a`).

**Success Criteria**:
Running `bash /home/user/project/ci.sh` must succeed (exit code 0). The generated `/home/user/project/output.json` must exactly contain the correctly resolved dependencies in JSON format.
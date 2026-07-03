You are a build engineer responsible for fixing a broken polyglot artifact resolution pipeline. The system processes a stream of package dependencies, compares their semantic versions against a baseline policy, and serializes the valid packages into a custom Trie structure.

The workspace is located at `/home/user/workspace/` and contains a partially complete CMake project. 

Your objectives:
1. **Vision / Policy Extraction:**
   There is a screenshot of the original Jira ticket detailing the baseline policy at `/app/ticket.png`. Extract the minimum semantic version constraint from this image (you will need to OCR or read it). All processed packages must be strictly greater than or equal to this version.

2. **Fix the Build System (CMake & Go):**
   The project contains a Go file (`engine.go`) designed to perform concurrent semantic version comparisons. 
   - Modify `CMakeLists.txt` to properly compile `engine.go` into a C-shared library named `libengine.so` during the CMake build process.
   - Complete `engine.go`. It must export a C-compatible function that takes an array of version strings and the baseline version constraint, spinning up goroutines to concurrently parse and compare standard Semantic Versions (Major.Minor.Patch). 

3. **Python Integration & Custom Data Structure:**
   Complete `/home/user/workspace/resolve.py`. 
   - Load `libengine.so` using `ctypes`.
   - Read a list of packages from `stdin` (format: `PackageName Version` per line).
   - Use the Go library to concurrently filter out any packages that do not meet the minimum semantic version from the image.
   - Insert the valid packages (just the package names) into a custom **Radix Trie** (Prefix Tree) data structure implemented in Python.
   - Serialize and print the Radix Trie to `stdout` in a pre-order traversal. Each node's string must be printed on a new line, indented by 2 spaces per depth level.

Ensure that running `cd /home/user/workspace/build && cmake .. && make` successfully builds the shared object, and that `python3 /home/user/workspace/resolve.py` correctly processes `stdin` to `stdout`.
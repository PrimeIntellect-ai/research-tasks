You are a developer building high-performance system utilities. Your current project requires a custom data structure—a Bloom Filter for strings—packaged as a shared library so it can be utilized by various scripting languages. You also need to guarantee its correctness using property-based testing.

Your task is to implement this shared library and its corresponding property-based test suite. You may use any programming language(s) you prefer, provided you meet the following requirements:

1. **Shared Library & ABI**:
   Create a shared library at `/home/user/project/libbloom.so`. It must expose the following exact C ABI (Action System V AMD64 ABI):
   - `void* bloom_create(int expected_elements, double false_positive_rate);`
     *Allocates and initializes the custom Bloom filter data structure. Returns an opaque pointer to it.*
   - `void bloom_add(void* bloom, const char* str);`
     *Hashes the null-terminated string and adds it to the Bloom filter.*
   - `int bloom_check(void* bloom, const char* str);`
     *Returns 1 if the string is probably in the filter, 0 if it is definitely NOT in the filter.*
   - `void bloom_destroy(void* bloom);`
     *Frees all memory associated with the Bloom filter fixture.*

2. **Custom Data Structure**:
   You must implement the Bloom filter logic yourself (do not just wrap an existing Bloom filter library, though standard math/hash libraries are fine). 

3. **Property-Based Testing & Fixtures**:
   Write a test suite using a property-based testing framework of your choice (e.g., `hypothesis` in Python, `QuickCheck` in Haskell, `proptest` in Rust). 
   The test suite must load the `libbloom.so` shared library and utilize test fixtures to properly create and destroy the Bloom filter for each test run to avoid state leakage.
   You must verify at least the following invariant property:
   - **No False Negatives**: If a set of randomly generated strings is added to the Bloom filter, `bloom_check` MUST return 1 for every single string in that set.

4. **Execution and Output**:
   Create a bash script at `/home/user/project/build_and_test.sh` that:
   - Compiles/builds the `libbloom.so` shared library.
   - Installs any necessary testing dependencies (e.g., via `pip`, `npm`, or `apt`).
   - Executes your property-based test suite.
   - If the tests pass, writes the exact string `SUCCESS: ALL PROPERTIES PASSED` to `/home/user/project/result.log`.

Constraints:
- All work must be contained within `/home/user/project/` (create this directory).
- Ensure your `build_and_test.sh` script is executable (`chmod +x`).
- Do not require root access for the test execution itself (use user-local package managers or `sudo` only for dependencies if absolutely necessary, assuming standard passwordless sudo is available in your environment).
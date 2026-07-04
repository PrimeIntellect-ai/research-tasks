You are a platform engineer maintaining a custom CI/CD pipeline. We recently designed a new lightweight build system DSL for our C projects to replace legacy Makefiles. To implement aggressive build caching, we need a utility to compute a deterministic "cache key" for any given build target by resolving its dependency graph.

Your task is to write a Rust program in `/home/user/cache_builder` that parses a build manifest, traverses the dependency graph, and calculates the final cache key for the target `release_bin`. 

The build manifest is located at `/home/user/build_graph.txt`.

**Manifest Format:**
Each line in the manifest defines a build target in the following format:
`TARGET_NAME: DEP1 DEP2 ... | COMMAND`
- `TARGET_NAME`: The name of the target.
- `DEP1 DEP2 ...`: A space-separated list of dependencies (other targets). This list may be empty.
- `COMMAND`: The exact shell command used to build the target (starts exactly one space after the `|` character, extending to the end of the line).

**Cache Key Calculation Rules:**
1. The cache key for a target is computed as the SHA-256 hash of a specific string.
2. The string to hash is constructed by concatenating:
   - The exact `COMMAND` string.
   - The computed cache keys of all its dependencies, appended in **alphabetical order of the dependency target names**.
3. All hashes must be lowercase hex-encoded strings. There should be no spaces or delimiters added during concatenation. 
4. The cache keys of dependencies must be fully resolved first (recursive evaluation).

**Example:**
If the manifest is:
```
lib_a: | gcc -c a.c
lib_b: | gcc -c b.c
app: lib_b lib_a | gcc a.o b.o -o app
```
- `lib_a` key = SHA256("gcc -c a.c")
- `lib_b` key = SHA256("gcc -c b.c")
- `app` key = SHA256("gcc a.o b.o -o app" + `lib_a` key + `lib_b` key)  *(Note: lib_a is appended before lib_b due to alphabetical sorting of the dependency names)*

**Objective:**
1. Initialize a Rust project in `/home/user/cache_builder`.
2. Write the logic to parse `/home/user/build_graph.txt` and compute the cache key for the target `release_bin`.
3. Your Rust program must output *only* the final 64-character lowercase hex SHA-256 hash for `release_bin` to a file located at `/home/user/cache_key.txt`.

You must write and execute this Rust program to generate the correct file. Do not hardcode the answer; your program must compute it based on the file contents.
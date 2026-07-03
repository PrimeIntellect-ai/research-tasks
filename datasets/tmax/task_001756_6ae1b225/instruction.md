I am a technical writer managing a massive repository of documentation bundles submitted by external contributors. These bundles are provided as ZIP archives. Before I ingest them into our main repository, I need to strictly filter out any invalid, malicious, or poorly-formatted archives. 

To do this, I need you to build a C++ CLI tool called `doc_filter` that analyzes a directory of ZIP files and classifies each one as either acceptable or invalid based on my documentation rules.

**Part 1: The Vendored Library**
I've provided the source code for a lightweight ZIP library, `miniz-cpp` (v0.1.0), located at `/app/vendored/miniz-cpp-0.1.0`. Unfortunately, the original author made a mistake in the `CMakeLists.txt` file which prevents it from building successfully. 
You must fix the build configuration, compile this library, and install it locally so you can link against it for the `doc_filter` tool.

**Part 2: Configuration Interpretation**
Your `doc_filter` tool must read a configuration file located at `/home/user/doc_rules.conf`. The file has the following key-value format:
```
ALLOWED_EXT=.md,.txt,.rst,.png
MAX_UNCOMPRESSED_TOTAL_MB=10
REJECT_HIDDEN=true
```
Your C++ program must parse these rules dynamically. 

**Part 3: Archive Verification and Search**
Your tool must take two arguments: the path to the config file, and the path to a directory containing ZIP archives.
Invocation: `./doc_filter /home/user/doc_rules.conf <target_directory>`

For every `.zip` file in the `<target_directory>`, the tool must:
1. Verify the archive's structural integrity (reject if corrupt).
2. Read the internal metadata of the files contained within the ZIP.
3. Reject the archive if it contains ANY file with an extension not listed in `ALLOWED_EXT`.
4. Reject the archive if the sum of the uncompressed sizes of all files exceeds `MAX_UNCOMPRESSED_TOTAL_MB`.
5. Reject the archive if it contains any hidden files or directories (names starting with `.`) and `REJECT_HIDDEN` is `true`.

**Output Format**
Your tool must print exactly one line to `stdout` for each archive in the directory, sorted alphabetically by the filename. The format must be:
`<filename>: CLEAN` (if it passes all rules)
`<filename>: REJECT` (if it fails any rule or is corrupt)

Example:
```
bundle1.zip: CLEAN
bundle2.zip: REJECT
```

Please place your compiled `doc_filter` binary at `/home/user/doc_filter`. Ensure it handles the adversarial test cases robustly!
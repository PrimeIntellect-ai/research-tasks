As a build engineer, you are responsible for managing our new artifact build system. We use a custom artifact metadata format `.art` which defines how artifacts are fetched, merged, and linked. 

We have a vendored Go library located at `/app/vendored/artparse` which implements a state machine-based parser for `.art` files. However, there are two problems you need to solve:

1. **Fix the Vendored Package**: The `artparse` library has a bug in its state machine implementation in `/app/vendored/artparse/parser.go`. It currently panics or enters an infinite loop when processing `MERGE` instructions because of a missing state transition. Identify and fix this bug so the package can be used reliably.

2. **Build the Artifact Filter**: We receive `.art` files from untrusted third-party build steps. You need to write a Go CLI tool at `/app/artifact-filter/main.go` that imports `artparse` and acts as a security filter. 
   - Compile your tool to the executable `/app/artifact-filter/filter`.
   - The executable must accept a single file path as a command-line argument: `./filter <path-to-art-file>`.
   - It must parse the file using the fixed `artparse` library.
   - It must analyze the parsed metadata and classify the artifact.
   - It must print exactly `ACCEPT` to standard output if the artifact is safe, or `REJECT` if it is unsafe. No other output should be printed to stdout.

**Safety Rules for Classification:**
An artifact MUST be classified as `REJECT` (unsafe) if ANY of the following apply:
- The artifact has a circular dependency in its `MERGE` chain (e.g., artifact A merges B, B merges C, and C merges A).
- Any `LINK` directive targets a path that attempts to escape the build directory (e.g., contains `../` or starts with `/`).
If the file cannot be parsed at all, it should be rejected.
If none of the unsafe conditions are met, the artifact MUST be classified as `ACCEPT`.

Ensure your tool correctly implements these rules. An automated verification suite will test your `/app/artifact-filter/filter` binary against an adversarial corpus of `.art` files.
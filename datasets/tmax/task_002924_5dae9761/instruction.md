You are an infrastructure engineer setting up a custom, polyglot build system from scratch. Your task is to write a Python-based build orchestrator that interprets a custom URL-based build Domain Specific Language (DSL), routes the build steps to a virtual emulator, and strictly sanitizes all inputs against malicious build configurations.

**Step 1: Extract the Build Token**
There is an architecture diagram located at `/app/build_architecture.png`. You must use OCR (e.g., `tesseract`) to extract the secret token required to authorize any build command. It will be labeled as `BUILD_TOKEN=<secret>`.

**Step 2: Implement the Build Orchestrator**
Write a Python script at `/home/user/build_orchestrator.py` that acts as the DSL interpreter and parameter parser. It must accept a file path containing a single build URL via a command-line argument:
`python3 /home/user/build_orchestrator.py --verify <file_path>`

**Build DSL Format:**
`build://{action}?token={BUILD_TOKEN}&target={target_name}&flags={compiler_flags}`

**URL Routing & Execution Rules:**
1. Parse the URL and validate the `token`. If it does not exactly match the token from the image, print `REJECT` and exit.
2. Route the `{action}`. Valid actions are strictly: `compile_c`, `compile_py`, and `link_bin`.
3. Extract `target` and `flags`. 
4. **Sanitization (Crucial):** You must detect and prevent command injection, path traversal, and malicious flags. 
   - `target` must only contain alphanumeric characters and underscores (no slashes, dots, etc.).
   - `flags` must only contain alphanumeric characters, hyphens, and spaces. Characters like `;`, `&`, `|`, `$`, `>`, `<`, or backticks must be strictly forbidden.
   - If any parameter is invalid, malicious, or missing, print `REJECT` and exit.
5. If the URL is clean and valid, act as an emulator for the build step. Print `ACCEPT: [{action}] built {target} with {flags}` to standard output.

**Step 3: Test Against the Adversarial Corpus**
We have provided two directories of test cases containing `.txt` files with single build URLs:
- `/app/corpus/clean/`: Contains entirely valid build URLs. Your script MUST accept all of these.
- `/app/corpus/evil/`: Contains malicious URLs attempting path traversals, command injections, or unauthorized actions. Your script MUST reject all of these.

You should thoroughly test your `build_orchestrator.py` against these corpora. An automated verifier will execute your script against both directories to ensure 100% of evil files are rejected and 100% of clean files are accepted and correctly simulated.
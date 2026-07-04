You are a mobile build engineer maintaining our CI/CD pipelines. We recently discovered that malformed or malicious dependency manifests (`MobileDep` format) have been crashing our build agents due to unresolved peer dependency conflicts and version downgrades. 

We are replacing our old validation script with a robust, high-performance Rust tool and integrating it into our multi-service ingestion pipeline.

Your objective is to build a Rust-based manifest validator, test it against an adversarial corpus of manifests, and integrate it into our multi-service pipeline.

### Part 1: The Rust Validator
In `/home/user/app/verifier/`, you will find a skeleton Rust project. You must implement the logic in `src/main.rs`. 
The binary should accept a file path as a CLI argument: `cargo run --release -- <file_path>`
- Exit code `0`: Manifest is valid (clean).
- Exit code `1`: Manifest is invalid (evil).

**The MobileDep Format & Parser State Machine:**
You must parse the file line-by-line using a strict state machine. The file must contain exactly these lines in this exact order:
1. `APP: <App_Name>`
2. `VERSION: <Major>.<Minor>.<Patch>`
3. `DEPS:`
4. Zero or more dependency lines formatted exactly as: `  - pkg: <name>, ver: <constraint>, resolved: <version>`
5. `END`

Any deviation in state order, missing lines, or extra unrecognized text must result in rejection (exit 1).

**Semantic Version Comparison (Numerical/Logical Component):**
For every dependency line, you must parse the `constraint` and the `resolved` version. 
Versions are strictly `<major>.<minor>.<patch>` (all integers).
You must support two constraints:
- `>=X.Y.Z`: The resolved version must be greater than or equal to X.Y.Z.
- `^X.Y.Z`: The resolved version must be greater than or equal to X.Y.Z, but strictly less than `(X+1).0.0` (assuming X > 0. If X=0, it must be less than `0.(Y+1).0`).

If any `resolved` version fails to satisfy its `constraint`, reject the file.

### Part 2: Adversarial Corpus
We have provided two directories of test files:
- `/home/user/corpora/clean/`: Contains 10 perfectly valid manifests. Your verifier MUST exit `0` for all of them.
- `/home/user/corpora/evil/`: Contains 15 malicious/malformed manifests (state machine violations, version downgrade attacks, bad constraints). Your verifier MUST exit `1` for all of them.

### Part 3: Pipeline Integration
The ingestion pipeline consists of:
1. **Redis**: Runs on standard port 6379.
2. **Gateway**: A Node.js service in `/home/user/app/gateway/`. It listens on port 8080.

The Gateway exposes `POST /submit`. It receives a manifest file in the request body. It currently lacks the validation step.
You must modify `/home/user/app/gateway/index.js` so that:
1. It writes the incoming manifest to a temporary file.
2. It executes your compiled Rust binary (`/home/user/app/verifier/target/release/verifier`) against the temp file.
3. If the Rust binary exits `0`, it pushes the manifest text to a Redis list called `valid_builds` and returns HTTP 200.
4. If the Rust binary exits `1`, it returns HTTP 400.

Start the Redis server, compile your Rust project, and start the Node Gateway service in the background so it is listening on port 8080 when you finish the task.
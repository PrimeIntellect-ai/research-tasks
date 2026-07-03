You are a script developer tasked with creating a utility to automate our CI/CD pipeline setup for a growing ecosystem of gRPC microservices. 

We have several microservices defined by Protocol Buffer (`.proto`) files located in `/home/user/protos/`. Services depend on each other, indicated by standard `import "filename.proto";` statements. To optimize our CI/CD pipeline, we want to build these services in parallel wherever possible, respecting their dependency graph.

Your task is to write a Python script at `/home/user/ci_gen.py` that parses these protobuf files, resolves the dependency graph, and generates a GitLab CI/CD configuration file (`/home/user/.gitlab-ci.yml`).

Specifically, the script must:
1. Scan `/home/user/protos/` for all `.proto` files.
2. Parse each file to find dependencies based on the `import "<filename>";` statements. (Assume all imports are in the same directory and just use the filename).
3. Compute the "build layer" for each service. 
   - A service with no imports is at Layer 0.
   - A service that imports other services is at Layer `N + 1`, where `N` is the maximum layer of all its dependencies.
4. Generate `/home/user/.gitlab-ci.yml` in the exact structure below.

The generated `.gitlab-ci.yml` must contain:
- A `stages:` array containing the stage names `stage_0`, `stage_1`, ..., up to the maximum layer computed.
- For each `.proto` file (e.g., `auth.proto`), a job block named `build_<filename_without_extension>` (e.g., `build_auth`).
- Each job block must specify its `stage:` (e.g., `stage_0` if it's layer 0).
- Each job block must have a `script:` array containing exactly one command: `echo "Building <filename_without_extension>"`

Example of expected YAML format:
```yaml
stages:
  - stage_0
  - stage_1

build_auth:
  stage: stage_0
  script:
    - echo "Building auth"

build_user:
  stage: stage_1
  script:
    - echo "Building user"
```

Once you have written the script, execute it so that `/home/user/.gitlab-ci.yml` is created. Do not use external libraries outside of the standard Python library (e.g., use `re` for parsing, do not install pyyaml—just write out the YAML structure as formatted text).
We are migrating our Kubernetes manifests to be managed by a custom Rust-based operator tool. The source code for this tool is pre-vendored on your system at `/app/k8s-manifest-gen`.

Your task is to fix, build, and configure this tool to run properly.

Currently, we are facing the following issues:
1. **Broken Build (Vendored Package):** The tool is failing to build. There is a deliberate error in its `Makefile` (an incorrect environment variable or command) that prevents `make build` from succeeding. You need to diagnose and fix the Makefile.
2. **Bloated Output (Metric Threshold):** Once built, the tool reads service JSON configurations from `/home/user/configs` and generates a combined YAML manifest at `/home/user/output/manifests.yaml`. However, a bug in the Rust source code (`src/main.rs`) causes it to duplicate Kubernetes Deployment resources wildly (creating 50 copies of each deployment). You must fix the Rust code so that it produces exactly one Deployment per service.
3. **Permissions & Execution:** The configuration directory `/home/user/configs` must have strict permissions. Write an idempotent bash script at `/home/user/run_operator.sh` that:
    - Sets the permissions of `/home/user/configs` to `0750` and ensures all files inside it are `0640`.
    - Builds the Rust tool using `make build` inside `/app/k8s-manifest-gen`.
    - Executes the built binary to generate the `/home/user/output/manifests.yaml` file.

**Success Criteria:**
- The bash script `/home/user/run_operator.sh` exists and successfully executes the pipeline.
- The output file `/home/user/output/manifests.yaml` is generated successfully.
- **Metric Verification:** The generated `manifests.yaml` file must be optimized. An automated test will measure the file size in bytes. Your fixed Rust code must produce a `manifests.yaml` that is **less than 2000 bytes**.

Please complete all steps using standard terminal commands and by modifying the files directly.
You are tasked with fixing and implementing a local Kubernetes manifest processing pipeline, conceptually similar to an admission controller but executed locally on raw files.

There are two main objectives:

1. **Fix the Vendored Utility:**
   We have a custom, proprietary package located at `/app/vendored/yaml-patcher-2.1.0`. This package provides a CLI utility to idempotently apply JSON patches or structural modifications to YAML manifests.
   Currently, the package is broken and cannot be installed. You must identify the perturbation in its configuration (e.g., a missing import or broken variable assignment in its build files) without requiring internet access. Fix the issue and install the utility locally for the `user`.

2. **Implement the Manifest Processor:**
   Write an executable program at `/home/user/manifest-processor`. You may write this in any language you choose (e.g., a bash script, Python script, or compiled Go program).
   
   **Requirements for `/home/user/manifest-processor`:**
   - It must read a single Kubernetes `Deployment` manifest (in YAML format) from `stdin`.
   - It must process the manifest to ensure that every container within the Deployment (`spec.template.spec.containers`) has a `volumeMount` named `audit-vault` mounted at `/var/log/audit`.
   - It must ensure that the Deployment's Pod spec (`spec.template.spec.volumes`) includes a volume named `audit-vault` of type `emptyDir: {}`.
   - The modifications must be idempotent. If the volume or volume mount already exists with the exact same name, it should not be duplicated.
   - It must output the modified YAML to `stdout` cleanly, retaining the semantic structure of the Kubernetes manifest.
   - You may use the repaired `yaml-patcher` utility, `yq`, `awk`, `sed`, or a scripting language with built-in YAML parsing to achieve this.

3. **Systemd Integration:**
   Create a user-level systemd service unit file at `/home/user/.config/systemd/user/manifest-watcher.service`. This service should be configured to execute a dummy script `/home/user/watch.sh` (you do not need to implement the watch logic, just create an empty executable file). Ensure the systemd configuration is valid and the service is enabled for the user.

Ensure your program at `/home/user/manifest-processor` is marked as executable (`chmod +x`). Automated testing will invoke your program via `stdin` with thousands of randomized Deployment manifests to verify BIT-EXACT equivalence against our reference oracle.
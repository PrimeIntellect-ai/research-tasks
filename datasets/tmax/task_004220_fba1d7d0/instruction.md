You are tasked with securing a local Git-based Kubernetes operator workflow. The operator processes Kubernetes manifests pushed to a local bare repository, passing them to an internal compiled validator.

However, the workflow is currently broken and insecure. You need to fix the environment, configure the required mock-mounts, set up correct permissions, and implement a robust sanitization filter as a Git pre-receive hook.

**Requirements:**

1. **Investigate the Validator Binary:**
   An internal tool is located at `/app/bin/manifest-compiler` (this is a stripped binary). It is designed to read a single YAML manifest from `stdin` and exit with code `0` if valid, or `1` if invalid. However, it currently crashes with an IPC socket error because it expects a specific socket workspace to be defined in its local mount configuration.

2. **Configure the Workspace and Fstab:**
   The binary reads `/home/user/operator/fstab.conf`. You must create this file. It must contain a single line defining a `tmpfs` mount for the directory `/home/user/operator/run` (which you must also create). The format of `fstab.conf` must perfectly match standard `fstab` syntax: 
   `tmpfs /home/user/operator/run tmpfs rw,nodev,nosuid,size=50M 0 0`
   
3. **Set ACLs:**
   The `manifest-compiler` strictly checks ACLs on `/home/user/operator/run`. You must use `setfacl` to ensure that ONLY the user `user` has `rwx` permissions, and default ACLs are also set to `user:user:rwx` for newly created files within it. Strip all permissions for group and others.

4. **Implement the Pre-receive Hook Filter:**
   The bare repository is located at `/home/user/k8s-manifests.git`. You must create a `pre-receive` hook at `/home/user/k8s-manifests.git/hooks/pre-receive`. This hook can be written in Bash or Python.
   
   The hook must:
   - Read the old revision, new revision, and ref name from standard input (standard Git `pre-receive` behavior).
   - Extract all `.yaml` files modified or added in the push.
   - For each file, pass the contents to `/app/bin/manifest-compiler` via standard input. If the compiler returns a non-zero exit code, the hook must reject the push.
   - **Crucially:** The `manifest-compiler` has a known bug. It incorrectly accepts manifests that mount the host's Docker socket (`/var/run/docker.sock`) or `containerd.sock`. Your hook must explicitly parse the YAML (using standard shell tools like `grep`, `awk`, or a Python script) and REJECT the push if ANY manifest attempts to define a `hostPath` volume pointing to `/var/run/docker.sock` or `/var/run/containerd.sock`. 
   - Accept the push only if all `.yaml` files pass both the binary validation and your `hostPath` security filter.

Your final deliverable is the properly configured environment and the `pre-receive` hook executable in the correct location.
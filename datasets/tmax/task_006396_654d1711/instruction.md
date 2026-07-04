You are building a lightweight, custom "GitOps" Kubernetes operator using C++ to manage local manifest deployments based on a simulated mount configuration.

The system administrator has created a mock `fstab`-like file at `/home/user/k8s_fstab` that maps Kubernetes namespaces to specific deployment directories. The file follows standard fstab column formatting:
`<namespace> <target_directory> <fs_vfs_type> <options> <dump> <pass>`

A bare Git repository exists at `/home/user/manifests.git`.

Your task is to write a C++ program and configure a Git hook to automatically deploy pushed Kubernetes manifests to their correct directories.

Step 1: Write and Compile the C++ Operator
Write a C++ program at `/home/user/operator.cpp` and compile it to `/home/user/operator` (using `g++ -std=c++17`).
The program must:
1. Accept exactly one command-line argument: a directory path containing Kubernetes YAML files.
2. Read the `/home/user/k8s_fstab` file to map namespaces to target deployment directories.
3. Iterate over all `.yaml` files in the provided directory.
4. For each `.yaml` file, find the namespace by looking for a line starting with `  namespace: ` (assume two spaces of indentation, followed by the namespace name). If no such line is found, default to the `default` namespace.
5. Copy the `.yaml` file to the target directory mapped to that namespace in `k8s_fstab`.
6. Append a log entry to `/home/user/operator.log` for every successful file copy, exactly in this format:
`Deployed <filename> to <target_directory>`
(where `<filename>` is just the basename of the file, e.g., `pod.yaml`).

Step 2: Configure the Git Hook
Create a `post-receive` hook in the bare Git repository at `/home/user/manifests.git/hooks/post-receive`.
The hook must:
1. Be written in Bash and be executable.
2. Extract the pushed contents of the `master` branch into a newly created temporary directory.
3. Execute the `/home/user/operator` program, passing the temporary directory as the argument.
4. Clean up (delete) the temporary directory after the operator finishes executing.

Assume you have access to standard Linux utilities (`grep`, `mktemp`, `git`, `g++`, etc.).
You are tasked with optimizing the manifest processing pipeline for a custom Kubernetes operator.

We have a proprietary, stripped binary located at `/app/k8s-manifest-processor` that minifies and validates Kubernetes YAML manifests. However, this legacy binary is highly inefficient and strictly interactive. 

Here is what you need to know about `/app/k8s-manifest-processor`:
1. It reads standard input interactively. When executed, it prints `Manifest path? > ` and waits for a single absolute file path. 
2. After receiving a path, it processes the file, writes the optimized manifest to the same directory with an `.opt.yaml` extension, and prints `Done.`. It then exits.
3. During processing, the binary attempts to connect to a hardcoded remote telemetry server at `10.254.254.10:8080`. Since this IP is unreachable in your environment, the network timeout causes a 2-second delay per manifest.

Your objective is to process a large directory of 500 Kubernetes manifests located at `/home/user/manifests/raw/` (you will need to generate these dummy files for testing) and output the optimized files. 

To accomplish this efficiently, you must write a Bash script at `/home/user/process_all.sh` that does the following:
1. **Network Redirection:** Uses `iptables` or firewall rules to intercept the binary's outgoing TCP connections to `10.254.254.10:8080` and redirects them to a local dummy server (e.g., a simple `nc` or `socat` listener, or a local Nginx reverse proxy) to bypass the 2-second timeout instantly.
2. **Interactive Automation:** Uses `expect` to programmatically interact with the `/app/k8s-manifest-processor` binary.
3. **Parallelization:** Wraps the `expect` script in a Bash pipeline (using `xargs -P` or `parallel`) to process multiple manifests concurrently, fully utilizing system CPU.

Before testing your script, create 500 valid dummy Kubernetes ConfigMap YAML files in `/home/user/manifests/raw/` (e.g., `cm-1.yaml` to `cm-500.yaml`). 

Your final solution will be evaluated based on the total execution time of `/home/user/process_all.sh`. A sequential execution without networking fixes would take over 1000 seconds. Your optimized, parallelized script with the telemetry timeout bypassed must complete processing all 500 files in **under 10 seconds**.

Ensure `/home/user/process_all.sh` is executable and entirely self-contained (starts the local dummy server, applies network rules, processes all files, and cleans up background processes).
You are tasked with fixing and optimizing a custom Kubernetes-operator-like tool written in Go, which simulates provisioning persistent volumes based on manifest files. The tool is currently failing when run via a scheduled script due to environment issues, writes to the wrong locations, and is far too slow to handle production scale.

Your objectives:

1. **Extract Configuration from Video:**
   There is a video file at `/app/operator_demo.mp4` that contains a recording of a flashing QR code. This QR code contains critical configuration parameters in the format `TARGET_DIR=<path>;BACKING_SIZE=<size>`.
   Use `ffmpeg` and `zbarimg` (you may need to install `zbar-tools`) to extract the frame and decode the QR code. 

2. **Fix the Environment Script:**
   The wrapper script `/home/user/run_operator.sh` is triggered by a simulated cron scheduler which runs with a highly restricted environment (`PATH=/bin`). Because of this, it currently fails to run the Go binary or standard tools, and mistakenly creates outputs in the root directory or fails entirely.
   Modify `/home/user/run_operator.sh` to:
   - Handle the `PATH` issue robustly so standard commands (like `mkdir`, `ln`, and the compiled Go binary) work.
   - Include standard bash error handling (fail fast on errors).
   - Pass the decoded `TARGET_DIR` and `BACKING_SIZE` from step 1 to the Go program via environment variables.

3. **Optimize and Fix the Go Operator:**
   The source code for the operator is at `/home/user/operator.go`. It processes 10,000 simulated YAML manifests located in `/home/user/manifests/`.
   Currently, the program processes these sequentially. You must modify `/home/user/operator.go` to process the manifests **concurrently** (using goroutines and a WaitGroup or workers) so that it completes the execution significantly faster.
   
   For each manifest (which contains a simulated Volume name and Namespace), the Go program must:
   - Create a simulated backing file of exactly `BACKING_SIZE` filled with null bytes (`\0`) at `$TARGET_DIR/<namespace>/<volume_name>.img`.
   - Append an fstab-like entry to `/home/user/fstab.mock` in the format:
     `$TARGET_DIR/<namespace>/<volume_name>.img /mnt/simulated/<namespace>/<volume_name> ext4 loop,defaults 0 0`
   - Create a relative symlink from `/home/user/active_mounts/<volume_name>` pointing to the generated `.img` file.

   *Note: Ensure all directory structures (`$TARGET_DIR/<namespace>`, `/home/user/active_mounts`) are created if they do not exist.*

4. **Integration & Building:**
   Compile your optimized Go program: `go build -o /home/user/operator /home/user/operator.go`.
   When you run `bash /home/user/run_operator.sh`, it must successfully process all 10,000 files, correctly populate `/home/user/fstab.mock`, and create the appropriate directory structure and symlinks.

Your ultimate goal is that running the script yields the correct filesystem state, and your Go program execution time is optimized to take less than 1.5 seconds.
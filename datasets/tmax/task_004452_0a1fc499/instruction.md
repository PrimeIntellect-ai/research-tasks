You are the maintainer of an open-source Web Application Firewall (WAF) simulator called `BashWAF`. A contributor has submitted a Pull Request (PR) to improve the system by adding a Go-based bytecode interpreter to safely sandbox and evaluate obfuscated web payloads. The Go library exposes its functionality via Cgo (FFI), which is then called by your primary Bash script `waf.sh` via a lightweight wrapper.

However, the PR is broken and the contributor is unavailable. Your task is to review, fix, and merge the PR.

Here are the requirements:
1. **Apply and Resolve Patch**: The contributor provided a patch file at `/home/user/pr.patch`. It modifies the existing `/home/user/bashwaf/waf.sh` and adds `/home/user/bashwaf/evaluator.go` and `/home/user/bashwaf/ffi_wrapper.py`. Attempting to apply the patch will result in a merge conflict in `waf.sh`. Resolve the conflict manually. You must keep the original `waf.sh` initialization checks, but use the new FFI wrapper logic from the patch.
2. **Fix Go Concurrency**: The `evaluator.go` implements a simple bytecode interpreter. However, the contributor introduced a deadlock in the goroutines/channels when processing the payload. Find and fix the concurrency bug in `/home/user/bashwaf/evaluator.go`.
3. **Build the FFI Library**: Compile the fixed `evaluator.go` into a C-shared library named `libeval.so` in the `/home/user/bashwaf` directory.
4. **Fix the Bash Script**: The PR introduced a bug in `waf.sh` regarding how it handles the FFI wrapper's return codes. Modify `waf.sh` to correctly interpret the exit codes from `ffi_wrapper.py`:
   - Exit code 0 means "CLEAN"
   - Exit code 1 means "MALICIOUS"
   - Exit code 2 means "ERROR"
   The script must append its final evaluations to `/home/user/bashwaf/scan_results.log` in the exact format: `<payload_id>: <STATUS>` (e.g., `req_001: MALICIOUS`).
5. **Run the tool**: Execute `./waf.sh /home/user/bashwaf/payloads.txt`. 

When you are done, the file `/home/user/bashwaf/scan_results.log` must contain the accurate evaluations of all payloads in `payloads.txt`.
We are porting an edge request validator to a minimal scratch container. The legacy C implementation was riddled with memory safety bugs and undefined behavior. We need you to rewrite it in safe Rust and compile it as a minimal binary.

Your task is to create a Rust program at `/home/user/limiter.rs` that performs basic request validation and rate-limiting, and compile it to `/home/user/limiter`.

The program must read lines from Standard Input (`stdin`) until EOF. Each line contains a request in the format: `IP,Path` (e.g., `192.168.1.1,/api/data`).

For each line, the program must evaluate the following rules in order and print exactly one line to Standard Output (`stdout`):
1. **Format Validation:** If the line does not contain exactly one comma separating two non-empty strings, output: `ERROR`
2. **Rate Limiting:** Track the number of times an `IP` has made *any* syntactically valid request (i.e., passed rule 1). If this is the 4th (or subsequent) request from this IP, output: `REJECT: <IP>`
3. **Path Validation:** If the `Path` does not start with the exact string `/api/`, output: `INVALID: <Path>`
4. **Success:** If all previous checks pass, output: `ACCEPT: <IP>`

To ensure the binary is small enough for our minimal container, you must compile it using standard Rust (`std` is fine) but optimized for size and stripped of symbols. Build the binary exactly like this:
`rustc -C opt-level=s -C strip=symbols /home/user/limiter.rs -o /home/user/limiter`

Once built, test your binary against the provided log file `/home/user/requests.log`. 
Run your program such that it reads from `/home/user/requests.log` and redirects its stdout to `/home/user/results.log`.
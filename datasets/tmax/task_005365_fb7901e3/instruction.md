You are an operations engineer triaging a severe incident. Our internal caching service has been experiencing out-of-memory (OOM) crashes due to a massive goroutine leak. We suspect this is being triggered by a specific, malformed network payload sent by a misbehaving client, which interacts poorly with a recent code change.

Your objectives:
1. **Pcap Analysis**: Analyze the network packet capture located at `/app/incident.pcap`. Identify the specific HTTP request signature (e.g., a specific combination of headers, paths, or payload) that is anomalous and causing the leak.
2. **Git Bisection & Fix**: The caching service's source code is a Git repository located at `/app/vendored/go-cache-server`. 
   - We know the tag `v1.0.0` is good, and `HEAD` is bad. 
   - Use `git bisect` to find the exact commit that introduced the goroutine leak.
   - Save the full 40-character SHA hash of the bad commit to `/home/user/bad_commit.txt`.
   - Fix the bug in the source code (it's likely a missing `defer`, unbuffered channel block, or context cancellation mishandling in `server.go`) so that the service no longer leaks goroutines.
3. **Adversarial Detector**: We need to filter out these malicious requests at our edge proxy before they hit the patched service. 
   - Write a Go program at `/home/user/detector.go` and compile it to `/home/user/detector`.
   - The CLI must accept a single argument: the path to a file containing a raw HTTP request.
   - Example invocation: `/home/user/detector /tmp/request.txt`
   - It must exit with code `1` if the request is "evil" (matches the signature causing the leak) and exit with code `0` if the request is "clean" (safe to process).

Ensure your detector is robust and accurately distinguishes the malicious payloads found in the pcap from normal traffic.
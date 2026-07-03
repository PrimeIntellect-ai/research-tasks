You are investigating a severe bug in a long-running packet analysis service written in Rust. The service processes network traffic and extracts custom TLV (Type-Length-Value) encoded metadata. Recently, the service has been experiencing hangs and rapid memory exhaustion (a massive leak due to infinite allocation) when processing certain traffic.

We have captured the problematic traffic in a pcap file located at `/home/user/capture.pcap`.

The source code for the service is in a local Git repository at `/home/user/packet-parser`. 
The master branch is currently failing (hanging/leaking) when it processes this pcap. 

Your tasks are:
1. Analyze the packet capture and the codebase to understand the parsing logic.
2. Use Git bisection to find the exact commit that introduced the regression causing the hang/leak.
3. Write the full 40-character commit hash of the offending commit to `/home/user/bad_commit.txt`.
4. Fix the infinite loop / recursion bug in the Rust code (specifically in `src/parser.rs`) so that the parser handles the malformed/edge-case packet correctly without hanging, looping infinitely, or panicking. It should gracefully skip or return an error for invalid lengths.
5. Ensure the project builds (`cargo build`) and can successfully process the pcap file by running `cargo run -- /home/user/capture.pcap` without getting stuck.

Provide the completed fix in the codebase and the `bad_commit.txt` file.
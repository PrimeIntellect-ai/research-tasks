You are an AI assistant helping a security researcher analyze a suspicious binary payload.

We have intercepted a large command-and-control (C2) beacon payload file located at `/home/user/payload.bin`. To analyze it, we wrote a custom parser in Rust, located in `/home/user/beacon_parser`. 

However, the parser crashes (panics) when processing the file. The malware authors seem to have included an anomalous frame with a malformed length field that triggers an out-of-bounds memory access error during slice extraction, crashing our analysis tool.

Your task is to:
1. Debug `beacon_parser` to find where the panic occurs.
2. Fix the format parsing edge-case in `/home/user/beacon_parser/src/main.rs`. Modify the parsing loop so that instead of panicking on an out-of-bounds slice access, it catches the bounds violation, prints "Anomaly detected at frame {frame_index}" (where `frame_index` is the 0-based index of the frame being processed), and gracefully stops processing further frames (break out of the loop and exit successfully).
3. Build and run the fixed parser on `/home/user/payload.bin`.
4. Redirect the standard output of the successful run to `/home/user/analysis_result.txt`.

The parser should be able to compile with `cargo build` without errors. Do not change the overall structure of the application, only fix the unsafe/panicking slice access in the main parsing loop by adding proper assertion-based intermediate validation.
You are an infrastructure engineer investigating an Out-Of-Memory (OOM) issue in a long-running Rust-based network service. The service processes custom binary payloads over TCP, but recently it has been leaking memory (specifically, `Arc` reference cycles generated during async task cancellation) when encountering specifically crafted malicious payloads. 

The previous on-call engineer left a screenshot of a memo before their shift ended, which contains the exact byte-level conditions that trigger the leak. You need to use this information to build a packet sanitizer.

Your tasks:
1. Extract the handwritten text from the image located at `/app/leak_memo.png` (using OCR tools like `tesseract` which are preinstalled). This memo contains the specific trigger condition for the malicious payloads.
2. Analyze the provided test network payloads.
3. Write a Rust-based CLI detector tool. Save your source code at `/app/detector.rs` and compile it to `/app/detector`.
4. Your compiled tool must accept a single command-line argument: the absolute path to a raw binary payload file.
5. The tool must parse the file and determine if it triggers the memory leak condition found in the memo.
   - If the file is a SAFE (clean) payload, the tool must exit with status code `0`.
   - If the file is a MALICIOUS (evil) payload that triggers the leak, the tool must exit with status code `1`.

We have provided two directories containing raw binary payloads for your testing:
- `/app/corpus/clean/` : Contains 50 well-formed payloads that do NOT trigger the leak.
- `/app/corpus/evil/` : Contains 50 malformed payloads that DO trigger the leak.

Ensure your compiled binary is executable and strictly adheres to the exit code requirements. The automated verifier will test your `/app/detector` against a hidden evaluation dataset.
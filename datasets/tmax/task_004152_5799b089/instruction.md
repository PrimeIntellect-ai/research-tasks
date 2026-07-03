You are a red-team operator working on an evasion exercise. Your colleague has exfiltrated a fragmented ELF payload via HTTP traffic, but the payload contains a signature that gets flagged by the target network's Intrusion Detection System (IDS).

You have been provided with an HTTP traffic log at `/home/user/traffic.txt`. The log contains multiple HTTP requests. The payload was exfiltrated in pieces within the `Cookie` headers of these requests. Specifically, the cookies are formatted as `Cookie: sequence=<N>; data=<hex_encoded_bytes>`, where `<N>` is the chunk order (starting at 0) and `<data>` contains the hex-encoded payload chunk.

Your task is to:
1. Extract and reassemble the hex-encoded payload chunks in the correct sequence from the HTTP headers in `/home/user/traffic.txt`.
2. Decode the reassembled hex into a raw binary file named `/home/user/reassembled.bin`.
3. Analyze the binary. You will find that it is a valid Linux ELF executable. However, it contains the plaintext signature `IDS_CATCH_ME` which triggers the IDS rule.
4. Write a Go program at `/home/user/evader.go` that reads `/home/user/reassembled.bin`, replaces the exact bytes of the signature `IDS_CATCH_ME` with `EVASION_DONE` (without corrupting the ELF structure or changing its size), and writes the modified payload to `/home/user/payload.bin`.
5. Run your Go program.
6. Set the file permissions of `/home/user/payload.bin` to exactly `0700` (executable only by the owner).

When you are finished, the automated test will verify the existence, permissions, and execution output of `/home/user/payload.bin`, as well as inspect the source code of your Go script.
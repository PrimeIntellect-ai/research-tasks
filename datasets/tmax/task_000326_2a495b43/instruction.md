You are a security researcher analyzing a suspicious network parser binary that is reportedly crashing in the wild.

Your threat intelligence team has provided a screenshot of a packet hex dump that triggers the exploit, located at `/app/packet_dump.png`. You also have the source code of the vulnerable binary at `/app/parser.c`. 

The binary crashes sporadically, but the threat intel payload triggers it deterministically. The vulnerability is believed to be related to a signed integer overflow when parsing packet lengths.

Your objectives:
1. Extract the hex string from the screenshot at `/app/packet_dump.png` (you can use `tesseract` which is installed on your system).
2. Convert the extracted hex string into a binary file.
3. Use delta debugging principles to minimize the binary payload to the absolutely smallest size (in bytes) that still triggers the exact same Segmentation Fault (exit code 139) in `/app/parser.c` (compiled with `gcc -o /app/parser /app/parser.c`).
4. Save your minimized binary payload to `/home/user/minimized_payload.bin`.
5. Identify the vulnerability in `/app/parser.c` and write a patched version that safely handles malicious lengths without crashing or truncating valid large packets. 
6. Save your patched source code to `/home/user/patched_parser.c`.

Requirements:
- Your patched C file will be evaluated against a hidden test suite of 100 malicious and benign payloads. 
- The metric to satisfy is the "Pass Rate", which must be exactly `1.0`.
- The size of your `minimized_payload.bin` must be 6 bytes or less, and it must successfully crash the *original* `/app/parser`.
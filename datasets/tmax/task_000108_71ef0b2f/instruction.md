You are a forensics analyst recovering evidence from a compromised host. We suspect the attacker exploited an open redirect vulnerability in the web server's login flow to deploy a custom rogue authentication binary, which generates forged session cookies to bypass access controls.

We have recovered two pieces of evidence:
1. A compiled binary located at `/app/rogue_auth.elf`. This binary analyzes HTTP headers and cookies, but primarily, it takes two command-line arguments: a `username` and an `origin_url` (from the HTTP Origin header), and outputs a forged session token string.
2. An image left by the attacker at `/app/ransom_note.png`. We suspect this image contains a handwritten or printed text string representing the cryptographic "salt" the binary uses internally to generate these tokens.

Your objective is to fully reverse-engineer the token generation logic and create a Python replica. 

Perform the following steps:
1. Inspect the image `/app/ransom_note.png` (you can use `tesseract` which is preinstalled) to extract the cryptographic salt.
2. Analyze `/app/rogue_auth.elf` to understand how it combines the username, the origin_url, and the salt to generate the final token. Look at the binary format and potentially use tools like `ltrace`, `strace`, `strings`, `objdump`, or write a script to fuzz it to infer its behavior. 
3. Write a Python script at `/home/user/token_generator.py`. This script must act as a perfect replica of the rogue binary's token generation function.
   - It must accept exactly two command-line arguments: `username` and `origin_url`.
   - It must print ONLY the generated token string to standard output.
   - It must correctly apply the salt recovered from the image.
   - The output must be bit-exact equivalent to the output of `/app/rogue_auth.elf` for any given input.

The automated test will rigorously fuzz your Python script against the original ELF binary with thousands of random inputs to ensure perfect equivalence.
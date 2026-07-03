You are an incident response network engineer investigating a suspicious connection. While inspecting network traffic, you intercepted a malicious C++ source file that compiles into an ELF payload. We suspect this payload embeds a backdoor SSH key in a custom ELF section and that the threat actor is transmitting further malicious ELF binaries over the network. 

Perform the following tasks to analyze the threat and secure the system:

1. **Compile and Analyze the Payload:**
   A suspicious source file is located at `/home/user/payload.cpp`. Compile it into an executable named `/home/user/payload` using `g++`.
   The attacker hid an SSH public key inside a custom ELF section named `.ssh_pub`. Extract the exact contents of this `.ssh_pub` section from the compiled binary and save it to `/home/user/found_key.pub`.

2. **Harden the SSH Configuration:**
   We need to allow the key for honeypot tracking but strictly isolate it. 
   Add the extracted SSH public key to `/home/user/.ssh/authorized_keys`. To prevent full access, you must prepend SSH hardening restrictions to this specific key entry. Specifically, restrict it to run a sandboxing script by prepending the following options (comma-separated, followed by a space before the ssh-key type):
   `command="/home/user/isolate.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty`

3. **Automated Traffic Scanning (C++):**
   We have a raw traffic capture dump at `/home/user/traffic.dat`. We need to find if another ELF binary was transmitted.
   Write a C++ program at `/home/user/scanner.cpp` that reads `/home/user/traffic.dat` in binary mode and searches for the standard ELF magic bytes (`0x7F 'E' 'L' 'F'`, or `\x7fELF`).
   The program must find the zero-based byte offset of the *first* occurrence of this magic sequence and write ONLY this integer offset to `/home/user/elf_offset.txt`.
   Compile and run your scanner to generate the output file.

Ensure all file paths and names match exactly.
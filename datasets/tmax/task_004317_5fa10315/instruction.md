You are acting as a security researcher analyzing a new strain of malware. We have intercepted some of its communications, but we need your help to build a functional C2 (Command and Control) emulator to interact with the infected nodes and study their behavior safely.

We have collected two crucial pieces of evidence:
1. `/app/intercepted.wav`: An audio recording of an automated analog beacon we intercepted over a radio frequency. It contains a sequence of DTMF (Dual-Tone Multi-Frequency) tones. We suspect the first 4 digits represent the C2 server's listening port, followed by a `*`, and then a 2-digit number which is the XOR key used for the payload encryption. 
2. `/app/traffic.pcap`: A network packet capture of the malware communicating with the real C2 server. 

Additionally, we have recovered a partial, broken C2 emulator script at `/home/user/broken_c2.c`. The original author was struggling with C structure serialization, network endianness, and memory leaks. It currently does not compile or function correctly.

Your objectives:
1. Analyze `/app/intercepted.wav` to extract the target port and XOR key.
2. Analyze `/app/traffic.pcap` to reverse-engineer the custom TCP communication protocol (pay attention to message framing, endianness, and how the payload is encoded).
3. Fix, complete, and compile `/home/user/broken_c2.c` into a working executable at `/home/user/c2_emulator`.
4. Run your emulator in the background so it binds to `0.0.0.0:<transcribed_port>`. It must continuously accept incoming TCP connections, correctly decode incoming messages using the key, and respond exactly as the real C2 server would when it receives the initialization handshake seen in the pcap.

The emulator must remain running so our automated verification suite can connect to it, perform the handshake, and validate its responses.
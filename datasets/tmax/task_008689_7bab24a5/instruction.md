You are a security researcher analyzing a suspicious C binary acting as a backdoor beacon. You have intercepted some network traffic and obtained the source code of the beacon. 

You have the following files in your environment:
1. `/home/user/beacon.c`: The source code of the suspicious beacon.
2. `/home/user/traffic.pcap`: A packet capture showing a successful command execution by the beacon.

Your analysis shows that the beacon listens on UDP port 8888 and uses a custom Type-Length-Value (TLV) encoding. However, the beacon's author made a critical mistake: it currently fails to correctly parse and execute commands that contain space characters (like `touch "/tmp/my file"`), silently truncating or mangling them.

Your task is to:
1. Analyze the `traffic.pcap` and `beacon.c` to understand the protocol and identify the parsing bug.
2. Fix the bug in `/home/user/beacon.c` so that the beacon correctly parses and executes commands containing spaces, while strictly respecting the provided length field in the payload. 
3. Compile the fixed binary to `/home/user/beacon`.
4. Write a Python regression test script at `/home/user/test_beacon.py`. This script must:
   - Construct a valid UDP payload using the beacon's TLV protocol.
   - The payload must instruct the beacon to execute the exact command: `echo "SPACE TEST" > /home/user/proof.txt`
   - Send the payload via UDP to `127.0.0.1:8888`.

Verification:
When you are finished, we will start your compiled `/home/user/beacon` in the background and run your `/home/user/test_beacon.py` script. Your solution is successful if the file `/home/user/proof.txt` is created and contains exactly `SPACE TEST`.
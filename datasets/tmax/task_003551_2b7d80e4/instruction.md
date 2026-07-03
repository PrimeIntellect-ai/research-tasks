You are a network engineer analyzing suspicious traffic on a company's internal network. You have intercepted a packet capture (`/app/traffic.pcap`) and a screenshot (`/app/intercepted_key.png`) that was sent to a suspicious internal host. Additionally, the incident response team recovered a stripped ELF binary (`/app/auth_client`) from the compromised machine.

Your objective is to build a Python-based traffic analysis tool that decodes the custom authentication payloads found in the network traffic.

Perform the following steps:
1. Extract the encryption key from `/app/intercepted_key.png`. You may use tools like `tesseract` to read the text from the image. The key is a 16-character alphanumeric string.
2. Analyze the `/app/auth_client` ELF binary. This binary generates the authentication payloads sent over TCP port 9090. You need to understand how it encodes the payloads (it uses a combination of basic XOR with the key and a specific binary format layout). 
3. Perform a local port scan to confirm the mock authentication service running on `localhost`. You can interact with it on port 9090 to test your decoding logic.
4. Write a Python script at `/home/user/decode_traffic.py`. The script must accept two arguments:
   - Arg 1: The path to a pcap file.
   - Arg 2: The extracted 16-character key.
   
The script must parse the provided pcap file, find all TCP payloads sent to port 9090, decode the payloads using the logic reversed from the ELF binary, and write a JSON file to `/home/user/decoded_payloads.json`.

The JSON file should be a list of objects, each containing:
- `packet_index`: The 1-based index of the packet in the pcap file.
- `username`: The decoded username string.
- `token`: The decoded authentication token string.

Your script must be highly accurate. It will be evaluated against a hidden, much larger pcap file (`/app/eval.pcap`) to determine its parsing and decoding accuracy. You must achieve an accuracy score of at least 0.95 (95%) to pass.
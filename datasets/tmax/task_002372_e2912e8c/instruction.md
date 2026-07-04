You are an edge computing engineer managing an IoT gateway deployment. You need to perform a staged deployment of a new telemetry parsing component, secure the existing configuration, and configure the local routing.

**1. Audio Transcription & Backup Strategy**
There is an audio file left by the previous engineer at `/app/maintenance_recording.wav`. Transcribe this audio file to retrieve the 4-digit maintenance PIN.
Write a backup script at `/home/user/backup.sh` that archives the directory `/home/user/iot_configs/` into a tarball and encrypts it using `openssl enc -aes-256-cbc -pbkdf2` with the PIN retrieved from the audio file as the passphrase. Output the encrypted file to `/home/user/configs_backup.tar.gz.enc`.

**2. Telemetry Parser Development (Go)**
You must write a Go program at `/home/user/telemetry_parser.go` to replace a legacy black-box component. 
The program must take a single command-line argument containing a Base64-encoded string. The program must:
a. Decode the Base64 string into a byte array.
b. Reverse the order of the bytes.
c. Print the resulting byte array as a lowercase Hexadecimal string to standard output, with no trailing newline.
Your Go implementation must be bit-for-bit perfectly equivalent to the legacy binary located at `/app/bin/ref_parser` for any valid Base64 input. Automated testing will fuzz your program against the reference binary with hundreds of random inputs.

**3. Rolling Deployment Script**
Write an automation script at `/home/user/deploy.sh` that performs a rolling deployment of your new Go parser. The script must:
a. Compile `/home/user/telemetry_parser.go` into an executable named `telemetry_parser`.
b. Iterate through the directories `/home/user/edge_nodes/node_1` to `/home/user/edge_nodes/node_5`.
c. For each node, copy the compiled `telemetry_parser` executable into the node's directory.
d. Create a file named `deploy.log` in each node's directory containing exactly the text: `Deployment successful`.
The script must process the nodes sequentially to simulate a staged rollout.

**4. Edge Port Forwarding**
Configure local port forwarding to route external edge traffic to the primary node. Since you do not have root access for `iptables`, use `socat` to forward TCP traffic from local port 8080 to local port 8081. Start this process in the background and ensure it persists.

Ensure all scripts (`backup.sh` and `deploy.sh`) are executable. You have all necessary standard tools (Go, openssl, socat, ffmpeg/whisper-cli) available in the environment.
You are an edge computing engineer managing a fleet of IoT devices. Due to a recent network misconfiguration during a Docker Compose deployment at our edge sites, many devices are unable to communicate with each other or the central server.

A field technician visited the site and left an audio memo at `/app/memo.wav`. You need to transcribe this audio file (you may install tools like `whisper.cpp` or use standard repositories) to retrieve two critical pieces of information:
1. The affected subnet (in CIDR notation).
2. The emergency backup recovery key.

Once you have these values, you must create a Go program that acts as a telemetry filter to identify which devices need the recovery sequence.

Write your Go program in `/home/user/telemetry_filter.go` and compile it to `/home/user/telemetry_filter`.

The compiled program `/home/user/telemetry_filter` must read from STDIN and write to STDOUT.
It will receive multiple lines of telemetry data, one per line, in the following format:
`<DeviceID>,<IPAddress>,<Status>`
(e.g., `edge-node-42,172.16.5.9,OFFLINE`)

For each line, your program must output a single line to STDOUT based on the following rules:
- If `<Status>` is exactly `OFFLINE` AND the `<IPAddress>` falls within the affected subnet (from the audio memo), output: `<DeviceID> RECOVER <BackupKey>` (where `<BackupKey>` is the exact string from the audio memo).
- Otherwise, output: `<DeviceID> IGNORE`

Example if the subnet was 10.0.0.0/8 and the key was "secret":
Input: `node-1,10.5.5.5,OFFLINE` -> Output: `node-1 RECOVER secret`
Input: `node-2,192.168.1.1,OFFLINE` -> Output: `node-2 IGNORE`

Requirements:
- Your Go program must handle standard CIDR parsing (e.g., using `net.ParseCIDR` and `Contains`).
- Malformed IP addresses should be treated as not matching the subnet.
- Ensure your binary is executable and located at `/home/user/telemetry_filter`.
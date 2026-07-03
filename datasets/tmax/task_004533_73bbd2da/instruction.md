You are a network engineer troubleshooting connectivity and log parsing for an internal application stack.

There are two primary objectives:

1. Multi-service connectivity fix:
An application stack is located in `/home/user/app`. It consists of a Web frontend (running on port 8000) and an API backend (running on port 8080). You can start the services using `/home/user/app/start.sh`.
Currently, the Web frontend is failing to communicate with the API backend. It seems it is trying to reach the API on the wrong port due to a misconfiguration in `/home/user/app/config.json`.
Update the configuration file so that the Web frontend properly connects to the API backend on port 8080. When configured correctly, an HTTP GET request to `http://127.0.0.1:8000/status` should return `{"status": "ok", "api_connected": true}`.

2. Packet log parsing script:
The API backend exports proprietary network packet logs in a specific hexadecimal format. A previous cron job was supposed to parse these, but it broke due to missing dependencies and PATH differences. You must write a fresh Python script at `/home/user/packet_parser.py` to parse these packets.
The script must read a single line of hexadecimal string from standard input (`sys.stdin`) and print the parsed result to standard output.

The packet structure (represented in the hex string) is as follows:
- 1 byte (2 hex chars): Version (unsigned integer)
- 2 bytes (4 hex chars): Total Packet Length (unsigned integer, big-endian). This length includes the header (version + length + timestamp).
- 4 bytes (8 hex chars): Timestamp (unsigned integer, big-endian)
- Remaining bytes: Payload.

Your script must print exactly:
`V:<version> LEN:<length> TS:<timestamp> DATA:<payload_ascii>`

Where `<payload_ascii>` is the payload decoded as ASCII characters. Any byte value outside the standard printable ASCII range (32 to 126 inclusive) must be replaced with a dot (`.`).
If the total length of the provided hex string is less than the header size (14 hex chars = 7 bytes), the script should output `INVALID_HEADER`.
If the length field in the header does not match the actual number of bytes provided, the script should output `LENGTH_MISMATCH`.

Example 1:
Input: `01000B0000000A74657374`
(Version 1, Length 11 bytes, Timestamp 10, Payload bytes 74 65 73 74 -> "test")
Output: `V:1 LEN:11 TS:10 DATA:test`

Example 2:
Input: `02000A0000000F610162`
(Version 2, Length 10 bytes, Timestamp 15, Payload bytes 61 01 62 -> "a.b" since 01 is not printable)
Output: `V:2 LEN:10 TS:15 DATA:a.b`

Ensure your script is executable (`chmod +x /home/user/packet_parser.py`) and uses `#!/usr/bin/env python3`.
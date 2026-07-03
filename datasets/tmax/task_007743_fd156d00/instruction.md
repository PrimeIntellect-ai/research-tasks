You are an on-call engineer responding to a 3am page. The automated data ingestion pipeline is randomly crashing. 

The pipeline uses a Python script `/home/user/process_telemetry.py` to extract UDP packet payloads from a network capture `/home/user/telemetry.pcap`. It writes each payload to a temporary file and processes it using a compiled C telemetry parser `/home/user/parser`. The `parser` binary is throwing a Segmentation Fault, bringing down the entire pipeline.

Your objective is to perform root cause analysis by combining packet capture analysis and binary debugging:
1. Identify the exact packet (0-indexed) in `/home/user/telemetry.pcap` that contains the malicious/malformed payload causing the crash.
2. Debug the `/home/user/parser` binary to understand the buffer overflow. Determine the exact 8-character ASCII string from the payload that directly overwrites the Instruction Pointer (RIP/return address) during the crash.

Write your findings to `/home/user/report.json` with the following strict format:
```json
{
    "crashing_packet_index": <integer>,
    "rip_overwrite_ascii": "<8-character string>"
}
```

Constraints & Notes:
- You have `gdb` and standard Linux tools available.
- You can install Python packages like `scapy` using `pip` if needed.
- Do not modify the `parser` binary or `telemetry.pcap`.
- The `rip_overwrite_ascii` should be the literal 8 bytes of the payload that end up in the instruction pointer, as text (e.g., "ABCDEFGH").
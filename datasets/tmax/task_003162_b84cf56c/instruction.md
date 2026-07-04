You are a tier-3 support engineer investigating a severe crash on a custom distributed key-value store. The server crashed after receiving a malformed payload, which also corrupted the tail of its Write-Ahead Log (WAL). 

Your objective is to collect diagnostics and recover the database state. You have two files provided in your home directory:
1. `/home/user/traffic.pcap`: A packet capture containing the recent network traffic to the server.
2. `/home/user/server.wal`: The binary Write-Ahead Log file, containing uncommitted database transactions.

**Phase 1: PCAP Analysis**
Identify the malformed network packet that triggered the crash. The packet was sent over TCP to port 9000 and contains the exact string payload `"POISON_PILL"`. 
Analyze the PCAP file to find the Source IP Address that sent this payload. 
Write the Source IP Address to `/home/user/attacker_ip.txt`.

**Phase 2: WAL Database Recovery**
Write a C++ program (save the source to `/home/user/recover.cpp`) that reads `/home/user/server.wal`, validates the entries, extracts the valid key-value pairs, and handles the corruption at the end of the file.

The `server.wal` file uses a custom binary format. It consists of a sequence of records. Each valid record follows this exact byte layout (all multi-byte integers are Little Endian):
- **Magic (4 bytes)**: Always the ASCII string `"KVLG"`.
- **Record Length (4 bytes, uint32_t)**: The total size in bytes of the remaining fields for this record (Opcode + KeyLen + Key + ValLen + Value + Checksum).
- **Opcode (1 byte)**: Action type. `0x01` represents a SET operation. Ignore any record that is not a SET operation.
- **Key Length (1 byte, uint8_t)**: Length of the key.
- **Key (N bytes)**: ASCII string.
- **Value Length (2 bytes, uint16_t)**: Length of the value.
- **Value (M bytes)**: ASCII string.
- **Checksum (1 byte)**: A simple XOR checksum. Starting with `0x00`, XOR every byte of the Opcode, Key Length, Key, Value Length, and Value. This must match the Checksum field.

*Corruption handling:* Due to the crash, the final record in the WAL is partially written. If a record's checksum is invalid, or if you encounter an unexpected EOF before a record is completely read, you must silently drop that record and stop parsing.

Your C++ program must compile cleanly (e.g., `g++ -O2 /home/user/recover.cpp -o /home/user/recover`). When executed, it must write the successfully recovered SET operations to `/home/user/recovered.txt`, with one record per line in the format: `Key=Value` (maintaining the exact order from the WAL).
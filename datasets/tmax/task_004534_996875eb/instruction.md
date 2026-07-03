You are tasked with debugging a failing build for a custom database recovery tool written in Rust. The tool is designed to reconstruct a corrupted database by replaying Write-Ahead Log (WAL) entries and applying a final state update received over the network.

Currently, the tool crashes with a Segmentation Fault (SIGSEGV) when processing a specific network packet.

Here is your workflow:
1. **Packet Capture Analysis:** You have been provided a packet capture file at `/home/user/traffic.pcap`. Find the single UDP packet destined for port `8888`. Extract its hexadecimal data payload and save the raw binary bytes to `/home/user/payload.bin`.
2. **Crash Debugging:** The Rust project is located at `/home/user/db_recovery`. It takes the network payload and the WAL file as arguments. If you run `cargo run -- /home/user/payload.bin /home/user/corrupted.wal`, it will panic or segfault. Use `gdb` or `rust-gdb` to inspect the crash.
3. **Code Fix:** Identify the memory safety issue (a buffer overflow in an `unsafe` block) in `src/parser.rs`. Fix the code by replacing the `unsafe` block with safe Rust slice operations or adding proper bounds checking so that malformed lengths do not cause out-of-bounds reads. If the length exceeds the available data, the function should safely truncate it to the available data length or return early.
4. **Database Recovery:** Once fixed, run the tool again. It will successfully process the WAL and the packet, generating a recovered SQLite database at `/home/user/recovered.db`.
5. **Data Extraction:** Query the `secrets` table in `/home/user/recovered.db` to retrieve the `recovery_key`. Save this key to `/home/user/flag.txt`.

Ensure your final flag is the only text in `/home/user/flag.txt`.
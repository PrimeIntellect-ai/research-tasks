You are a DevOps engineer trying to recover database logs from a crashed server. The server's network interfaces died, but its diagnostics system blinked an error code on a diagnostic LED, which a local technician recorded on video. 

The video is available at `/app/transmission.mp4`.

Your analysis of the system documentation reveals the following about the video's encoding:
1. The video flashes solidly colored frames.
2. Each frame represents a single bit of an ASCII text message.
3. A purely black frame (`#000000`) represents the bit `0`. A purely white frame (`#FFFFFF`) represents the bit `1`.
4. The bits are transmitted sequentially to form 8-bit ASCII characters (Most Significant Bit first).

**Your objectives:**
1. Extract the bitstream from `/app/transmission.mp4` to decode the hidden ASCII specification message.
2. The decoded message will provide precise rules for reversing a data corruption issue that occurred in the server's Write-Ahead Log (WAL).
3. Based on the rules in the decoded message, implement a minimal reproducible Python script at `/home/user/recover.py`.
4. Ensure `/home/user/recover.py` strictly follows the input/output signature and data transformation logic described in the decoded message.

Automated verification will aggressively fuzz your `/home/user/recover.py` script against a hidden reference implementation using thousands of random inputs to ensure it is bit-exact equivalent. Ensure your script handles zero-padding and exact formatting correctly!
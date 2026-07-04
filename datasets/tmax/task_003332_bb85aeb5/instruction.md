You are a security researcher analyzing a new strain of malware. We have isolated a suspicious executable at `/app/suspicious_bin`. This binary acts as an encoder/decoder for the malware's command and control (C2) communications. 

We also managed to intercept a screen recording of the attacker's C2 dashboard, located at `/app/c2_dashboard.mp4`. We need you to reverse-engineer the encoding algorithm and create a bit-exact Python replica of the binary.

Your tasks are:

1. **Video Forensics & Query Result Debugging**:
   Extract frames from `/app/c2_dashboard.mp4` (you can use `ffmpeg`). The video contains a scrolling log of C2 query results. At exactly 2.5 seconds into the video, a query result debug message flashes on the screen containing the 4-byte Initialization Vector (IV) used by the algorithm, formatted as `INIT_IV: 0x[HEX]`. Recover this IV.

2. **System Call Tracing & Timeline Reconstruction**:
   Use `strace` or similar tools on `/app/suspicious_bin` to observe its behavior. Notice how it processes inputs. The binary takes a single command-line argument (a string) and outputs a hex-encoded string. 

3. **Formula Implementation Correction**:
   We have provided a draft implementation at `/home/user/decoder.py`. The original analyst made mistakes in the bitwise arithmetic formula and failed to apply the correct IV. 
   Debug and fix `/home/user/decoder.py` so that it correctly implements the algorithm. It must:
   - Accept a single string as a command-line argument.
   - Use the IV extracted from the video.
   - Output the exact same hex-encoded string as `/app/suspicious_bin`.

Your final deliverable is the corrected `/home/user/decoder.py`. An automated test will randomly fuzz both `/app/suspicious_bin` and your Python script with hundreds of inputs to ensure 100% bit-exact equivalence.
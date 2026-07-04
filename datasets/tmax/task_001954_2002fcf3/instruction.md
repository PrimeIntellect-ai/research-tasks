You are a forensics analyst investigating a compromised host. We have secured an evidence container, but the attacker used complex obfuscation and left behind a mixture of legitimate admin scripts and malicious persistence mechanisms. 

There are two stages to your investigation:

**Stage 1: Key Recovery from Video Evidence**
The attacker encoded the decryption key for their toolset into a single frame of a screen recording captured during the breach. 
1. The video file is located at `/app/evidence/screen_capture.mp4`.
2. Extract the frames of this video. Exactly one frame contains a cleartext string in the format `KEY-{32_hex_chars}`. 
3. Use this key to decrypt the AES-256-CBC encrypted archive located at `/app/evidence/scripts.tar.gz.enc`. The password for the decryption is the full `KEY-{32_hex_chars}` string.
4. Extract the decrypted archive to `/home/user/forensics/scripts/`. This will yield two directories: `evil/` and `clean/`, containing samples of the attacker's scripts and our legitimate system scripts, respectively.

**Stage 2: Adversarial Script Detector**
You need to write a Rust-based detection tool to automatically classify these scripts, as we expect to find more of them across our fleet.
1. Create a Rust project at `/home/user/forensics/detector`.
2. Your tool must be compiled to an executable at `/home/user/forensics/detector/target/release/detector`.
3. The tool should take a single command-line argument: the path to a directory containing script files.
4. For every file in the directory, your tool must analyze the contents and determine if it is malicious or clean. The attacker's scripts always try to evade basic sandboxing by checking for containerized environments or specific file permissions before executing their payload, while legitimate scripts do not contain these evasion checks.
5. Your tool must print exactly one line per file to standard output in the format: `[EVIL|CLEAN]: <filename>`. Example:
   `EVIL: update_service.sh`
   `CLEAN: backup_cron.sh`

Your detector must correctly classify 100% of the scripts in the provided `evil/` and `clean/` directories. Furthermore, an automated verification suite will test your compiled binary against a hidden adversarial corpus of similar scripts to ensure your detection logic is robust and doesn't just hardcode filenames.
You are an artifact manager responsible for curating binary repositories. We have recently detected a supply chain attack where malicious actors embedded a specific, hidden binary signature into our artifacts.

We captured a video recording of the attacker's terminal during the incident, which we managed to recover. This video is located at `/app/incident_record.mp4`. The exact binary signature (a sequence of hex bytes) used in the attack is embedded in the video's subtitle/text track (Stream #0:2). 

Your objective is to:
1. Extract the hex signature from the video file at `/app/incident_record.mp4` using tools like `ffmpeg`, `sed`, or `awk`.
2. Write a Rust program located at `/home/user/classifier.rs` and compile it to `/home/user/classifier`. 
3. The Rust program must take a single file path as a CLI argument. It should return exit code `0` if the file is CLEAN (does not contain the signature) and exit code `1` if the file is EVIL (contains the signature).
4. For performance reasons, your Rust program MUST use memory-mapped I/O (`memmap2` crate is available in the environment) to scan the file for the extracted signature.
5. We have provided a test corpus of artifacts. Recursively traverse `/app/corpus/incoming/`. For every file found:
   - Run your classifier.
   - If clean, create a hard link to the file in `/home/user/repo_verified/`.
   - If evil, create a symbolic link to the file in `/home/user/repo_quarantine/`.

Ensure your classifier is highly accurate. We will run an automated test against your `/home/user/classifier` binary using a separate, hidden adversarial corpus containing known clean and known evil files to verify its accuracy.

Both `/home/user/repo_verified/` and `/home/user/repo_quarantine/` must be created by you.
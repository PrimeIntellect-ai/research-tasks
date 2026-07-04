We are rotating SSH credentials for our legacy backup servers. Unfortunately, the old key generation utility (`/app/keygen_legacy`) is a stripped binary, and the original source code is lost. To make matters worse, the binary requires a specific activation phrase to run, which was left as a voicemail by the former sysadmin.

Here is what you need to do:
1. Listen to or transcribe the audio file located at `/app/voicemail.wav`. It contains the activation phrase needed to unlock the binary.
2. Reverse engineer the `/app/keygen_legacy` ELF binary to understand its custom key derivation algorithm. It takes a seed string as an argument and outputs a deterministic pseudo-random sequence used for the keys.
3. Once you understand the algorithm, write a pure Bash script at `/home/user/keygen_recreated.sh` that perfectly replicates the behavior of `/app/keygen_legacy`.
4. Your Bash script must accept a single argument (the seed string) and output the exact same sequence of bytes as the original binary to standard output.
5. As part of the credential rotation, configure the SSH daemon in the local environment (config at `/home/user/sshd_config`) to disable password authentication and only allow Ed25519 keys, representing standard SSH hardening.

Your script at `/home/user/keygen_recreated.sh` will be rigorously fuzzed against the original binary to ensure bit-exact equivalence. Ensure it handles arbitrary seed strings correctly.
You are a network engineer assisting with a security incident. We intercepted a suspicious transmission from a compromised server. The capture resulted in two artifacts:
1. An encrypted audio transmission saved at `/app/intercepted_comms.wav`.
2. A stripped Linux ELF binary found on the compromised host, located at `/app/oracle_decoder`.

Through preliminary analysis, we know the following:
- The audio file contains a spoken sequence of phonetic characters/digits which acts as the master decryption key for the binary. You will need to transcribe this audio file (you may install and use tools like `whisper` or `ffmpeg` to process it).
- The `oracle_decoder` binary uses this master key, combined with a custom cryptographic hashing and XOR-based encryption algorithm, to process arbitrary input payloads. 
- The binary is invoked as: `/app/oracle_decoder <master_key> <hex_encoded_payload>` and prints the resulting processed hex string to stdout.

Your objective is to:
1. Extract the master key from the audio file.
2. Reverse engineer the `/app/oracle_decoder` binary to understand its custom cryptographic algorithm.
3. Write a C++ program at `/home/user/my_decoder.cpp` that perfectly replicates the behavior of the oracle binary. 
4. Compile your C++ program to `/home/user/my_decoder`.

Your implementation must be BIT-EXACT equivalent to the `oracle_decoder` for any arbitrary hex-encoded payload when provided the correct master key. The testing suite will fuzz your compiled binary against the original oracle with thousands of random payloads to ensure the cryptographic logic matches exactly. 

Ensure your final compiled executable is located precisely at `/home/user/my_decoder` and accepts arguments in the exact same format: `/home/user/my_decoder <master_key> <hex_encoded_payload>`.
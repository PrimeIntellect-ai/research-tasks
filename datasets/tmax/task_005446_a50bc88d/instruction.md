You are a forensics analyst recovering evidence from a compromised web server. We have discovered that the attacker left behind a stripped binary, `/app/oracle_bin`, which they used to decrypt exfiltrated web traffic payloads. They also left behind their vendored source code for `libsodium` in `/app/libsodium-1.0.18`, but they deliberately sabotaged the source code to prevent us from building our own analysis tools.

Your task consists of two parts:

1. **Fix the Vendored Library**: The attacker modified a file within the `/app/libsodium-1.0.18` source tree to introduce a compile-time error. Locate the deliberate syntax error, fix it, and compile/install the library locally in `/home/user/local_libsodium`.

2. **Replicate the Decryptor**: Write a C++ program at `/home/user/decryptor.cpp` and compile it to `/home/user/decryptor`. Your program must behave EXACTLY like `/app/oracle_bin`. 
   - Both programs take two arguments: `argv[1]` is a hex-encoded ciphertext, and `argv[2]` is a 2-byte hex string representing the first half of a 4-byte decryption key.
   - Your program must brute-force the remaining 2 bytes of the key (from `0000` to `FFFF`).
   - For each guess, attempt to decrypt the ciphertext using libsodium's `crypto_secretbox_open_easy` (assume a hardcoded zeroed nonce).
   - If decryption succeeds (returns 0) and the plaintext starts with the string "HTTP/1.1", print the plaintext to `stdout` and exit with code 0.
   - If the keyspace is exhausted without a match, print "DECRYPTION FAILED" to `stderr` and exit with code 1.

The automated verification system will extensively fuzz your `/home/user/decryptor` binary against the `/app/oracle_bin` oracle with random inputs to ensure bit-exact equivalence in stdout, stderr, and exit codes.
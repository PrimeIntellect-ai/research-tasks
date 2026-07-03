You are a security researcher analyzing a suspicious binary. You have recovered the source code for a custom decryption tool written in Rust by the malware author, located at `/home/user/malware_decoder`. It is supposed to decrypt a payload located at `/home/user/evidence.enc` and write the result to `/home/user/decrypted.txt`.

However, the tool currently crashes during execution due to an internal assertion failure at byte index 50: `thread 'main' panicked at 'Integrity check failed at byte 50'`. 

Through prior reverse-engineering of the malware, we know the following about the decryption algorithm:
1. It uses a rolling `state` variable initialized to `0xAF`.
2. Each byte is decrypted by XORing it with the current `state`.
3. The `state` is then updated for the next iteration using a modulo addition. 
4. The malware author made an algorithmic mistake in the state update logic within `src/main.rs` (likely confusing whether the state should be updated using the *encrypted* byte or the *decrypted* byte).

Your task:
1. Navigate to `/home/user/malware_decoder`.
2. Use a debugger (like `rust-gdb`), intermediate state tracing (`println!`), or data transformation diff analysis to inspect the intermediate variables right before the panic.
3. Identify and fix the algorithmic bug in the `decrypt` function inside `src/main.rs`. 
4. Compile and run the fixed code so that it successfully decrypts `/home/user/evidence.enc` and saves the full plaintext to `/home/user/decrypted.txt`.

The automated verification test will check the exact contents of `/home/user/decrypted.txt`. Do not add any extra newlines or metadata to the final output file.
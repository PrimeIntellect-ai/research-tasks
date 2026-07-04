You are a DevSecOps engineer responsible for enforcing "Policy as Code" for a set of internal applications. You have been provided a set of newly built binaries in the directory `/home/user/pipeline_binaries/`. You must audit these binaries for privilege escalation risks and cryptographic weaknesses.

Your task has three phases:

**Phase 1: Privilege Escalation Auditing**
According to our security policy, no binary deployed in the pipeline should have the SUID (Set-User-ID) bit set.
1. Scan the directory `/home/user/pipeline_binaries/` for any files with the SUID bit set.
2. Write the absolute paths of all violating binaries to `/home/user/suid_violators.txt`, one path per line, sorted alphabetically.

**Phase 2: ELF Analysis and S-Box Extraction**
One of the binaries, `/home/user/pipeline_binaries/custom_crypto_auth`, contains a proprietary block cipher implementation. Our cryptography policy states that custom S-boxes must be audited for differential cryptanalysis vulnerabilities.
1. Analyze the ELF binary `custom_crypto_auth`.
2. Extract the contents of the 8-bit S-box, which is stored in a public symbol named `CUSTOM_SBOX`. The S-box is exactly 256 bytes long.
3. Save the extracted 256 bytes exactly as raw binary data to `/home/user/extracted_sbox.bin`.

**Phase 3: Differential Cryptanalysis in Rust**
You must analyze the extracted S-box to determine its maximum differential uniformity.
1. Create a new Rust project in `/home/user/ddt_analyzer/` (e.g., using `cargo new`).
2. Write a Rust program that reads `/home/user/extracted_sbox.bin`.
3. Compute the Differential Distribution Table (DDT) for the 8-bit S-box.
4. Find the maximum differential uniformity (the highest value in the DDT, excluding the trivial case where the input difference is 0).
5. The Rust program must write this single integer value (in base 10) to `/home/user/max_diff.txt`.

Ensure your Rust code compiles and runs successfully to produce `/home/user/max_diff.txt`. You may use any terminal tools (e.g., `readelf`, `objcopy`, `dd`, `bash`) alongside your Rust code.
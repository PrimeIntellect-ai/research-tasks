You are a security engineer preparing to rotate user credentials. To migrate accounts securely, you must verify the integrity of the legacy credentials during the login flow before re-hashing them with a modern algorithm.

We use a custom, lightweight ARX (Add-Rotate-Xor) hashing algorithm for legacy accounts. However, the vendored Go package for this algorithm at `/app/vendored/legacyhash` contains a recently introduced bug. A typo in the core mixing round destroys the data entropy, compromising its resistance to differential cryptanalysis and causing all our legacy file integrity and checksum verifications to fail.

Your task is to fix this and provide an executable for the migration pipeline:

1. Inspect the source code in `/app/vendored/legacyhash/mixer.go`. The inline comments explicitly state the intended bitwise operation (a 64-bit cyclic left shift by 13 bits), but the current implementation is flawed due to a typo in the bitwise shift logic. Fix this bug.
2. Create a Go program at `/home/user/hash_runner.go`. 
   - It must import the local module (module path is `legacyhash`). Note: You may need to set up a `go.mod` in `/home/user` that uses a `replace` directive to point `legacyhash` to `/app/vendored/legacyhash`.
   - It must take a single string as the first command-line argument (`os.Args[1]`).
   - It must pass this string to `legacyhash.Hash([]byte(input))` which returns a `uint64`.
   - It must print this `uint64` to standard output as a 16-character, zero-padded, lowercase hexadecimal string followed by a newline (e.g., `fmt.Printf("%016x\n", result)`).
3. Compile your program to `/home/user/hash_runner`.

We have provided a stripped reference binary of the legacy implementation at `/opt/oracle/legacyhash_oracle`. You can use this to verify your fixes. Running `/opt/oracle/legacyhash_oracle "test"` should yield the exact same hex output as `/home/user/hash_runner "test"`. An automated fuzzer will verify that your compiled binary perfectly matches the oracle's output for random inputs.
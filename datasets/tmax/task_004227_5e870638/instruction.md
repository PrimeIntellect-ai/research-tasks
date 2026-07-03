We are currently in the middle of a massive credential rotation operation. Our legacy credential generation system uses a proprietary standalone tool, located at `/app/credgen_legacy`. This tool takes a base64-encoded seed string via standard input, performs a custom decoding and hashing sequence, and prints a final hexadecimal credential hash.

Unfortunately, this legacy binary is incredibly slow because it spawns a heavily isolated sandbox for each invocation. We have a file containing 100,000 base64-encoded seeds at `/app/seeds.txt`. Processing all of these using a bash loop with the legacy tool will take hours, which is unacceptable for this security rotation.

Your task is to:
1. Analyze the `/app/credgen_legacy` binary to determine its exact cryptographic hashing and payload decoding logic.
2. Write a highly optimized C program at `/home/user/fast_credgen.c` that replicates this exact logic. Your program should read seeds from a specified input file (one per line) and output the rotated credential hashes to a specified output file (one per line).
3. Compile your program to `/home/user/fast_credgen`.
4. Run your program using `/app/seeds.txt` as the input and save the generated credentials to `/home/user/rotated_creds.txt`.

Your optimized C implementation must be functionally equivalent to the legacy binary. Furthermore, it must meet strict performance requirements: your compiled program must process the entire 100,000-line input file in under 0.25 seconds. 

Ensure your C program is self-contained and relies only on standard libraries or OpenSSL (which is installed).
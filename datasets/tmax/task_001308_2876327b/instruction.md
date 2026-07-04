You are an open-source maintainer reviewing a broken Pull Request (PR) for a web security library that generates audio CAPTCHAs. The PR replaces the token signing algorithm with a custom, high-performance C hashing function to prevent timing attacks. However, the PR is broken and the contributor left some crucial information out of the code.

Here is the situation:
1. The contributor provided an audio voice note at `/app/pr_voice_note.wav` explaining a missing Initialization Vector (IV) required to make the algorithm match the backend server.
2. The server's reference implementation is provided as a stripped binary at `/app/oracle_bin`. It reads from `stdin` and prints a 32-bit hex string to `stdout`.
3. The broken PR code is located in `/home/user/pr_repo/fasthash.c`. It contains a custom hashing algorithm using inline assembly and numerical manipulations, but it fails to compile, has performance benchmarking stubs that crash, and uses a placeholder IV of `0x00000000`.

Your tasks:
1. Use a transcription tool (like Whisper or ffmpeg+pocketsphinx) to listen to `/app/pr_voice_note.wav` and extract the 32-bit hex Initialization Vector (IV).
2. Fix the compilation and logic errors in `/home/user/pr_repo/fasthash.c`. The code should correctly implement a byte-by-byte hash where `hash = (hash ^ byte) * 0x01000193`, seeded with the IV from the audio.
3. Compile the fixed code to an executable at `/home/user/fasthash_fixed`.
4. The executable `/home/user/fasthash_fixed` must take arbitrary binary data from `stdin` and output the lowercase 8-character hex string of the final 32-bit hash to `stdout`, matching `/app/oracle_bin` EXACTLY for any input.

Ensure your compiled program runs cleanly. Automated testing will intensely fuzz your `/home/user/fasthash_fixed` against `/app/oracle_bin` to ensure bit-exact equivalence over thousands of random inputs.
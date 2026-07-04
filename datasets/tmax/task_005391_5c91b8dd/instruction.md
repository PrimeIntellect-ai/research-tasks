As an MLOps engineer, you are building a lightweight C++ utility to track experiment outputs and compute an embedding signature based on a reference video artifact. We need a fast, standalone C++ program to validate model outputs by computing a hash-like embedding tied to the reference video.

Write a C++ program at `/home/user/embedder.cpp` and compile it to an executable named `/home/user/embedder`.
The program must process inputs from standard input (stdin) line by line. For each line, it will compute and print a 4-dimensional integer embedding.

Here are the precise rules for computing the embedding:
1. The reference artifact is located at `/app/experiment_video.mp4`.
2. When the program starts, it must read exactly the first 4096 bytes of `/app/experiment_video.mp4` into memory. Treat these as 4096 `unsigned char` values. (You can assume the file is larger than 4096 bytes).
3. Process standard input line by line. For each line, remove the trailing newline character (`\n` or `\r\n`).
4. If a line is perfectly empty (length 0), the program should output exactly `0,0,0,0` followed by a newline, and move to the next line.
5. For a non-empty line of length `L`, initialize a 4-element integer array (or vector) `emb` to zeros: `emb[0] = 0, emb[1] = 0, emb[2] = 0, emb[3] = 0`.
6. The 4096 bytes are conceptually divided into 4 chunks of 1024 bytes. For each chunk `i` (from 0 to 3):
   For each byte index `k` in the chunk (from 0 to 1023):
     a. Let `byte_val` be the unsigned char value from the file at absolute index `i * 1024 + k`.
     b. Let `char_val` be the ASCII value of the character in the input line at index `k % L`.
     c. Update the embedding dimension: 
        `emb[i] = (emb[i] + byte_val * (char_val + 1)) % 10007;`
7. After processing all 1024 bytes for all 4 chunks, print the embedding for the line as a comma-separated string (no spaces): `emb[0],emb[1],emb[2],emb[3]` followed by a newline.
8. The program must cleanly exit when it reaches EOF on standard input.

You may use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<string>`, `<vector>`). Do not use any external dependencies. Ensure your executable is compiled and placed at `/home/user/embedder`.
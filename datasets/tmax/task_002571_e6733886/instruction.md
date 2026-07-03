You are a bioinformatics analyst tasked with building a sequence classifier to detect a specific synthetic DNA motif.

We have received a video file at `/app/primer_synthesis.mp4`. This video is exactly 20 seconds long, encoded at 1 frame per second. Each frame consists of a solid background color that represents a single nucleotide in a 20-base synthetic primer sequence. The color mapping is as follows:
- Red (pure red, e.g., #FF0000) = A
- Green (pure green, e.g., #00FF00) = C
- Blue (pure blue, e.g., #0000FF) = G
- Yellow (pure yellow, e.g., #FFFF00) = T

Your task:
1. Extract the frames from `/app/primer_synthesis.mp4` to decode the 20-base synthetic primer sequence. You may use standard CLI tools like `ffmpeg` and `ImageMagick` (`magick` / `convert`) to analyze the frames.
2. Write a C program and compile it to `/home/user/detector`. 
3. The executable `/home/user/detector` must take exactly one argument: the path to a plain text file containing a single, continuous DNA sequence (consisting only of A, C, G, T) on a single line.
4. The program must scan the given sequence to find if the 20-base synthetic primer occurs anywhere within it. A match is considered valid if there are **3 or fewer mismatches** (substitutions) compared to the exact 20-base primer. No gaps or indels need to be considered.
5. If a valid match is found, the sequence is classified as "evil", and your program must immediately terminate with **exit code 1**.
6. If no valid match is found anywhere in the sequence, the sequence is classified as "clean", and your program must terminate with **exit code 0**.
7. Because the input sequences can be extremely long, you must use **OpenMP** (`#pragma omp parallel for`) in your C code to parallelize the sliding-window search. The code should be compiled with `-fopenmp`.

During verification, an automated test suite will run `/home/user/detector <file>` against two hidden corpora: a clean corpus where no sequences contain the primer, and an evil corpus where every sequence contains the primer. Your program must correctly reject 100% of the evil corpus (exit code 1) and accept 100% of the clean corpus (exit code 0).
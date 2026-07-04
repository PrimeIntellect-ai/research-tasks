You are acting as a bioinformatics analyst. We are trying to process a set of DNA sequences, but our pipeline is currently broken and non-deterministic.

Here is what you need to do:
1. We have an audio file `/app/primer.wav` which contains a dictated target primer sequence (e.g., someone reading out "A T G C..."). You will need to transcribe this audio to recover the exact primer sequence.
2. We have a FASTA file `/app/reads.fasta` containing several sequence reads.
3. There is a C++ program at `/app/analyze.cpp` that takes a primer sequence as a command-line argument, adds it to the list of sequences from `reads.fasta`, computes an all-pairs Smith-Waterman alignment score matrix, and then uses power iteration to find the leading eigenvalue of this matrix.
4. Unfortunately, `analyze.cpp` uses OpenMP for parallelism and has a bug in its power iteration loop: the floating-point reduction order is non-deterministic (or has a race condition), leading to slightly different and incorrect results on every run. 
5. Fix the OpenMP reduction bug in `/app/analyze.cpp` so that the result is strictly deterministic and mathematically correct. 
6. Compile the fixed C++ program and run it using the primer sequence you transcribed from the audio file.
7. The program will output the leading eigenvalue. Save this exact floating-point number to a file named `/home/user/eigenvalue.txt`.

Ensure your C++ code is correct and that the floating-point reduction properly computes the dot product and norm required for power iteration without race conditions.

You may use any transcription tools (like whisper, ffmpeg, or python libraries) you need to process the audio.
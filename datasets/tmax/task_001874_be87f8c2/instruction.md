I am a researcher organizing a massive collection of raw numerical datasets. My PI left me a short voice memo with instructions on how we need to filter the incoming data streams for our experiment tracking pipeline, but I am deaf and cannot listen to it. 

The audio file is located at `/app/dataset_note.wav`.

Please do the following:
1. Transcribe the audio file to find out the specific numerical smoothing algorithm and the precise parameter (`alpha`) we are supposed to use. You can use any available tools (like ffmpeg or python libraries) to extract the speech.
2. Write a C++ program at `/home/user/ema_filter.cpp` that implements this exact algorithm.
3. The program must read a continuous stream of raw 32-bit floats (IEEE 754 little-endian) from `stdin` until EOF.
4. For each float `x_t` read, compute the filtered value `y_t` using the algorithm and parameter from the audio, and write `y_t` out as a raw 32-bit float to `stdout`.
5. Assume the standard initialization where the first output equals the first input (`y_0 = x_0`). Ensure proper numerical accuracy by consistently using single-precision `float` types.
6. Compile your program to an executable named `/home/user/ema_filter` using `g++ -O3`.

Do not add any text output, headers, or formatting to `stdout`—it must strictly output the raw binary floats so it can be piped seamlessly in our bash pipelines.
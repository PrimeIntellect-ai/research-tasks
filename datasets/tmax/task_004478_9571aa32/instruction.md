I need help organizing a large dataset for our project using a custom C++ tool. I have an offline environment, but I've pre-placed the source code for the `miniz` compression library at `/app/miniz-3.0.2`.

Unfortunately, the Makefile for `miniz` seems to be broken—it's failing to build. 

Here is what you need to do:
1. Fix the `miniz` library at `/app/miniz-3.0.2` so it compiles successfully into a static library (`libminiz.a`).
2. We have a raw dataset located at `/home/user/dataset/` containing two types of files: `.log` (text) and `.dat` (binary).
3. Write a C++ program at `/home/user/organizer.cpp` that links against `libminiz.a`.
4. Your C++ program must iterate through `/home/user/dataset/`.
5. For every `.log` file, strip out the timestamps at the beginning of each line (format: `[YYYY-MM-DD HH:MM:SS] `) using a text transformation approach, keeping the rest of the line.
6. For every `.dat` file, extract only the first 16 bytes (the binary header).
7. Concatenate the transformed log data and the extracted binary headers, and compress the combined stream using `miniz` into a single deflate-compressed archive at `/home/user/organized.bin`. 
8. **Crucial Requirement**: You must configure the `miniz` compression level to achieve maximum compression (`MZ_BEST_COMPRESSION` or level 9). We have a strict size quota, and the final `organized.bin` must be smaller than the threshold of 85,000 bytes. 

Please build your C++ tool, process the dataset, and generate the final `/home/user/organized.bin` file.
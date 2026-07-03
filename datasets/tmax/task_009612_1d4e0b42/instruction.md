You are a data scientist tasked with cleaning and aligning two spatial datasets from different sensor networks. You have two datasets, `/home/user/sensors_A.csv` and `/home/user/sensors_B.csv`. Both files have the following header and format:
`id,x,y,z`
The coordinates `x`, `y`, and `z` are floating-point numbers.

Your task is to write a reproducible pipeline to join these multi-source datasets based on spatial similarity (nearest neighbor). 

Perform the following steps:
1. Write a C program located at `/home/user/matcher.c` that:
   - Reads both CSV files.
   - For every sensor in dataset A, finds the nearest sensor in dataset B using Euclidean distance.
   - Handles numerical accuracy properly using double-precision floats.
   - Outputs the results to a new file `/home/user/matches.csv`.

2. The output file `/home/user/matches.csv` must exactly match this format:
   - Header row: `id_A,id_B,distance`
   - Data rows: comma-separated, with the distance formatted to exactly 4 decimal places (e.g., `1,5,12.3456`).
   - The rows should be ordered by `id_A` ascending.

3. Create an executable bash script located at `/home/user/pipeline.sh` that acts as your reproducible pipeline. It must:
   - Compile `/home/user/matcher.c` into an executable named `/home/user/matcher` using `gcc` and linking the math library (`-lm`).
   - Run the compiled `matcher` executable to generate `/home/user/matches.csv`.

Ensure your C code gracefully handles parsing the CSV headers and iterates correctly.
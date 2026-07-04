You are a performance engineer tasked with building a highly optimized baseline data parser for a new spectroscopy sensor. The sensor outputs a continuous stream of signal amplitudes as a flat text file, which actually represents multiple observational sweeps.

Your task is to write a Rust program that reshapes this 1D data into a 2D array, decomposes the spectral domain into sub-meshes, computes the maximum signal intensity in each mesh, and validates it against a known analytical threshold.

Here are the specific requirements:
1. There is a raw data file located at `/home/user/data/signal.txt` containing 400 floating-point numbers, one per line.
2. Write a Rust program at `/home/user/spectral_profiler.rs`.
3. The program must read `signal.txt` and reshape it into a 2D array (or equivalent structure) representing 4 observations (rows), where each observation contains 100 spectral bins (columns).
4. Perform a domain decomposition by splitting the 100 spectral bins into 4 equal sub-meshes (25 bins each). So Mesh 0 contains bins 0-24, Mesh 1 contains 25-49, Mesh 2 contains 50-74, and Mesh 3 contains 75-99.
5. For each of the 4 sub-meshes, calculate the maximum signal value across *all* 4 observations.
6. Validate each maximum against an analytical threshold of `40.0`. If the maximum is strictly greater than 40.0, the status is `VALID`, otherwise it is `INVALID`.
7. The Rust program must print exactly 4 lines to standard output in the following format:
   `Mesh <ID>: <MAX_VALUE> - <STATUS>`
   (Ensure the floating-point number is formatted to exactly one decimal place, e.g., `18.0`).

Once the program is written:
1. Compile it using `rustc -O /home/user/spectral_profiler.rs -o /home/user/spectral_profiler`.
2. Run the executable and redirect its standard output to `/home/user/mesh_validation.log`.

Do not use any external crates; standard library Rust is sufficient. The entire process should be executed in the terminal.
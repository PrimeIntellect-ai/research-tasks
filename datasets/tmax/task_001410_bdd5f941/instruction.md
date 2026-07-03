I need you to build a bioinformatics pipeline that processes the output of an experimental DNA sequencing machine. The machine outputs its raw sensor readings as a video file showing fluorescent intensity matrices over time, rather than text sequences. 

Your task is to build a reproducible pipeline in C++ that extracts these frames, reconstructs the nucleotide probability matrices via matrix decomposition, and runs an optimization to find the most likely sequence.

Here are the specific requirements:

1. **Video Processing**: There is a raw sensor output video at `/app/fluorescence_sensor_run01.mp4`. Use `ffmpeg` to extract the frames. Each frame is a grayscale image representing a 16x16 sensor array. 
2. **Signal Matrix Reconstruction**: Write a C++ program named `seq_extractor` (in `/home/user/src/`) that compiles to `/home/user/bin/seq_extractor`. This program must:
    - Take a path to a directory containing the extracted grayscale frame images as its first command-line argument.
    - Read each frame, converting the 16x16 pixel intensities (0-255) into a `double` matrix.
    - Perform Singular Value Decomposition (SVD) on each frame's matrix to extract the dominant spatial feature (the first left singular vector).
    - Map the components of this vector to a custom 4-dimensional nucleotide space using a given basis (which is provided in `/app/nucleotide_basis.csv`).
3. **Optimization Step**: For each frame, use a gradient-based optimization approach (or simplex) to find the nearest valid pure sequence state (a vector with exactly one '1' and three '0's) to the projected 4D vector, outputting the characters A, C, G, or T.
4. **Integration**: The tool must output a single contiguous string of characters (one per frame, chronologically) to standard output. 
5. **Visualization**: Create a shell script `/home/user/plot_singular_values.sh` that calls an external visualization tool (like Python/matplotlib, which you can set up) to plot the ratio of the first singular value to the sum of all singular values over time (saving it to `/home/user/svd_variance.png`).

Ensure your C++ program relies only on standard libraries, `stb_image` (available in `/app/vendor/`), and the `Eigen` library (which you should download and configure as part of the compilation). Your executable will be fuzz-tested against our reference oracle using various sets of synthetic frame directories to ensure bit-exact equivalence of the sequence output.
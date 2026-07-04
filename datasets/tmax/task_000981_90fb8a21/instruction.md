You are assisting a computational chemistry researcher running simulations on molecular network models. The pipeline models these molecules using adjacency matrices, but the simulation software frequently crashes with a "ZeroDivisionError" or similar numerical instability when it encounters near-singular matrices (ill-conditioned molecular graphs).

To fix this, you need to build a data sanitization pipeline that filters out these near-singular matrices before they enter the simulation.

Here are your instructions:

1. **Compile the Analysis Tool:**
   The researcher has written a small C utility that computes the determinant of these adjacency matrices using LU decomposition. The source code is located at `/app/src/calc_det.c`. Compile this source code into an executable named `calc_det` and place it in `/home/user/bin/` (create the directory if it doesn't exist).

2. **Extract the Threshold:**
   The exact numerical threshold for the determinant to distinguish between "stable" (clean) and "near-singular" (evil) molecular graphs is written in a scanned lab note. The image is located at `/app/lab_notes_scan.png`. You will need to extract this threshold (tesseract is installed on the system).

3. **Create the Sanitizer Script:**
   Write a pure Bash script at `/home/user/filter_graph.sh`.
   - The script must take exactly one argument: the path to a matrix text file.
   - It should use your compiled `calc_det` tool to compute the determinant of the given matrix.
   - It should compare the absolute value of the determinant against the threshold you found in the image. (You may use standard CLI tools like `awk` or `bc` within your Bash script to do the floating-point comparison).
   - If the absolute determinant is **strictly less than** the threshold, the matrix is considered "evil" (near-singular) and your script must **exit with code 1**.
   - Otherwise, the matrix is "clean" and your script must **exit with code 0**.
   - Your script must be executable.

We will test your `/home/user/filter_graph.sh` against a hidden adversarial corpus of "evil" and "clean" matrix files. Your script must correctly reject 100% of the evil matrices and accept 100% of the clean matrices.
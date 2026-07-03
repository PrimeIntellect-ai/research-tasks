You are a data scientist analyzing fluid dynamics experiments. We extract spatial covariance embeddings from video frames using matrix factorization. However, sensor glare in some frames produces near-singular pixel matrices, causing our downstream C++ factorization pipeline to produce NaNs and crash.

Your task is to build a C++ pre-filter to sanitize the inputs, test it against an adversarial corpus, and then apply it to a new experimental video.

**Step 1: Environment & Implementation**
1. Install any necessary libraries for C++ matrix operations (e.g., Eigen3), video processing, and Python-based visualization.
2. Write a C++ program at `/home/user/filter.cpp` that:
   - Takes a single command-line argument: the path to a text file containing a space-separated 64x64 matrix of floating-point numbers.
   - Loads the matrix.
   - Computes the condition number $\kappa$ (the ratio of the largest to the smallest singular value).
   - Prints exactly `REJECT` to standard output if $\kappa > 10000$ or if the smallest singular value is extremely close to zero. Otherwise, prints exactly `ACCEPT`.

**Step 2: Adversarial Corpus Validation**
We have provided a corpus of matrices to test your filter:
- `/app/corpus/clean/`: Contains 20 text files with well-conditioned 64x64 matrices. Your C++ program must output `ACCEPT` for 100% of these.
- `/app/corpus/evil/`: Contains 20 text files with near-singular 64x64 matrices (glitch simulations). Your C++ program must output `REJECT` for 100% of these.
Compile your program to `/home/user/filter` and ensure it passes this test.

**Step 3: Video Processing & Orchestration**
We have a new experimental video located at `/app/fluid_flow.mp4`.
1. Extract the frames from this video at exactly 10 frames per second.
2. Convert each frame to a 64x64 grayscale image.
3. Export each 64x64 image as a space-separated text file of pixel intensities (0.0 to 255.0).
4. Run your compiled C++ `/home/user/filter` on every frame's text file.
5. Create a log file at `/home/user/rejected_frames.txt`. This file must contain the 1-based frame numbers (e.g., frame 1 is the first extracted frame) of all frames that were `REJECT`ed, sorted in ascending order, one integer per line.

**Step 4: Experimental Visualization**
Create a Python script that reads the condition numbers of all extracted frames (in chronological order) and plots them as a line chart. Save this visualization to `/home/user/cond_plot.png`.

Ensure your C++ code is robust and your final `/home/user/rejected_frames.txt` contains only the strictly required frame numbers.
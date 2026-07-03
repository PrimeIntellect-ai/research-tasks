I am a researcher organizing a massive dataset of laboratory video observations. I am building a custom pipeline to index these videos based on structural motion, but I need your help to implement the core feature extraction and model training components. 

My pipeline has two parts: video preprocessing (which I'd like you to write in Python) and an online learning model (which must be written in C++ for performance).

**Step 1: Video Preprocessing**
I have a sample video located at `/app/experiment.mp4`. 
Write a Python script at `/home/user/extract.py` that reads this video and extracts its frames as follows:
1. Extract frames at exactly 2 frames per second.
2. Convert each frame to grayscale.
3. Resize each frame to 16x16 pixels.
4. Normalize the pixel intensities to be between 0.0 and 1.0 (float32).
5. Flatten each frame into a 256-dimensional vector.
6. Append all frames sequentially into a raw binary file at `/home/user/dataset.bin` (which should contain exactly $N \times 256$ float32 values, where $N$ is the number of extracted frames).

**Step 2: Online Model Training**
I have a compiled reference binary at `/app/oracle_model` that computes a tracking signature, but the source code was lost. I need you to rewrite it in C++.
Write a C++ program at `/home/user/model.cpp` and compile it to `/home/user/model_exec`.

The program must accept exactly one command-line argument: the path to a `.bin` file (like the one generated in Step 1) containing $N$ consecutive 256-dimensional float32 vectors.

The algorithm must perform the following online linear regression training:
1. Initialize a weight vector $W$ of size 256, where every element is set to `0.100000`.
2. For each 256-dimensional frame vector $X_i$ in the file (from $i=0$ to $N-1$):
   a. Compute the prediction: $y = \sum_{j=0}^{255} X_{i,j} \cdot W_j$
   b. Compute the error against a target of 1.0: $error = y - 1.0$
   c. Update the weights: $W_j = W_j - (0.001 \times error \times X_{i,j})$ for all $j \in [0, 255]$.
3. After processing all frames, print the final 256 weights to standard output, separated by spaces, with exactly 6 decimal places of precision (e.g., using `printf("%.6f ", W[j])`). Print a final newline.

Ensure `/home/user/model_exec` is fully deterministic and exactly matches the algorithm described, as it will be rigorously tested against the oracle using random binary files. Finally, run your compiled program on `/home/user/dataset.bin` and save the output to `/home/user/signature.txt`.
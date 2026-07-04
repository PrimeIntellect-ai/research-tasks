You are an AI assistant helping a data researcher clean up a large collection of sensor datasets. The researcher has a mix of valid recordings and corrupted ("evil") adversarial recordings that need to be filtered out before downstream training.

You need to build a C++ filtering utility that extracts features from the datasets and runs them through a predefined neural network model to classify them.

Here are the specific requirements:

1. **Vendored CSV Parser Configuration**
   The researcher relies on a fast C++ CSV parser, vendored at `/app/csv-parser` (vincentlaucsb/csv-parser v2.1.3). However, the researcher accidentally modified its `CMakeLists.txt` and now it refuses to build in their projects because it is requesting the wrong C++ standard. 
   - You must fix the perturbation in `/app/csv-parser/CMakeLists.txt` so it correctly requires C++17.

2. **Feature Engineering**
   Write a C++ program at `/home/user/detector.cpp` that accepts a CSV file path as a command-line argument. The CSV files have a header row and four columns: `timestamp`, `sensor_x`, `sensor_y`, `sensor_z`.
   Using the fixed `/app/csv-parser`, read the file and extract the following three features across all rows:
   - $f_1$: The arithmetic mean of `sensor_x`
   - $f_2$: The maximum absolute value of `sensor_y`
   - $f_3$: The root mean square (RMS) of `sensor_z`. (RMS is the square root of the mean of the squares).

3. **Model Architecture Reconstruction**
   The researcher has already trained a small Multi-Layer Perceptron (MLP) to detect the corrupted files based on these features. You must implement the forward pass in C++ from scratch (do not use external ML libraries like TensorFlow or PyTorch).
   
   **Architecture:**
   - Input layer: 3 features ($f_1, f_2, f_3$)
   - Hidden layer: 2 neurons, ReLU activation function: $f(x) = \max(0, x)$
     - Weights $W_1 = \begin{bmatrix} 0.5 & -0.2 & 0.1 \\ -0.1 & 0.8 & 0.0 \end{bmatrix}$ (Row 1 is for Neuron 1, Row 2 is for Neuron 2)
     - Biases $b_1 = \begin{bmatrix} 0.0 \\ -0.5 \end{bmatrix}$
   - Output layer: 1 neuron, Sigmoid activation function: $\sigma(x) = \frac{1}{1 + e^{-x}}$
     - Weights $W_2 = \begin{bmatrix} 1.5 & -1.0 \end{bmatrix}$
     - Bias $b_2 = 0.2$
     
   Calculate the final output probability. If the output is $\ge 0.5$, print exactly `EVIL` to standard output. If the output is $< 0.5$, print exactly `CLEAN` to standard output.

4. **Integration**
   Create a bash script at `/home/user/run_filter.sh` that takes a single file path as an argument. The script should invoke your compiled C++ program on that file and return exit code 0 if the file is cleanly parsed and predicted as `CLEAN`, and exit code 1 if it is predicted as `EVIL`.

Your final deliverables should be the fixed `CMakeLists.txt`, the `detector.cpp` source code, the compiled binary, and the executable `run_filter.sh` wrapper.
You are a machine learning engineer preparing a feature extraction pipeline for sensor network data. 

First, we have an image containing handwritten system parameters located at `/app/system_params.png`. Please extract the text from this image (you can use tools like `tesseract`). It contains four key parameters in the format:
`ROOT=<node_id> TARGET=<node_id> BAND_MIN=<freq_bin> BAND_MAX=<freq_bin>`

Second, there is a graph representing the sensor network topology in `/app/sensor_graph.txt`. The first line is the number of vertices `V` and the number of edges `E`. The following `E` lines contain pairs of connected nodes (undirected edges, uniform weight of 1).

You need to write a C++ program and compile it to `/home/user/feature_extractor` (it must be a standalone binary).

The program must do the following:
1. Read exactly 64 floating-point numbers from standard input (`stdin`), separated by whitespace. This represents a single sensor's time-series window ($y_0, y_1, \dots, y_{63}$ with $x$ implicitly being $0, 1, \dots, 63$).
2. Calculate the linear regression line $y = mx + c$ for these 64 points.
3. Compute the Discrete Fourier Transform (DFT) magnitudes for the input signal.
4. Find the frequency bin index (from $0$ to $31$) that has the maximum DFT magnitude, restricted *strictly* to the inclusive range `[BAND_MIN, BAND_MAX]` obtained from the image.
5. Compute the shortest path distance (number of edges) between the `ROOT` node and the `TARGET` node using the graph provided in `/app/sensor_graph.txt`.
6. Print the results to standard output (`stdout`) as a single space-separated line:
   `[SLOPE] [INTERCEPT] [MAX_FREQ_BIN] [SHORTEST_PATH_DIST]`
   Format the slope and intercept to exactly 4 decimal places.

Compile your program with `g++ -std=c++17 -O3`. Your compiled binary will be heavily fuzzed against a reference implementation to ensure identical bit-exact output for various random input sequences.
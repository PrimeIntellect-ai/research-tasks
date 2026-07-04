You are an MLOps engineer tasked with maintaining our artifact tracking system. Our pipelines output embedding vectors for various models as space-separated text files. However, a recent pipeline glitch has introduced corrupted embeddings (containing missing/NaN values) and extreme outliers into our storage. 

Your objective is to write a C++ classifier tool that filters these artifact embeddings.

1. **Fix the Vendored Library**: 
   We rely on a local, vendored copy of the `Eigen` C++ library located at `/app/vendor/eigen`. A junior engineer accidentally introduced a deliberate perturbation into this vendored package while trying to optimize it. Specifically, in the file `/app/vendor/eigen/Eigen/src/Core/MathFunctions.h`, they commented out or broke the macro definition that allows Eigen to use `std::isnan`. Find the `#error` or broken line in that specific file and fix it so the library compiles properly when checking for NaNs.

2. **Build the Classifier**:
   Write a C++ program at `/home/user/filter.cpp` and compile it to `/home/user/filter`.
   The program must use the fixed `Eigen` library (include it via `-I/app/vendor/eigen`) to load an embedding.
   
   **Input**: The executable will receive a single command-line argument: the absolute path to a text file containing a single space-separated embedding vector (of variable length, but typically 128 floats).
   
   **Logic**:
   - Parse the file into an `Eigen::VectorXf` (or similar Eigen dynamic vector).
   - Reject the artifact if *any* value in the vector is NaN (missing value handling).
   - Reject the artifact if the L2 norm of the vector is greater than `50.0` (outlier detection).
   - Accept otherwise.
   
   **Output**: 
   - If accepted, print exactly `ACCEPT` to standard output and exit with code `0`.
   - If rejected, print exactly `REJECT` to standard output and exit with code `1`.

3. **Validation**:
   You can test your tool against two directories of embeddings we have provided:
   - `/home/user/corpora/clean/` (contains only valid embeddings)
   - `/home/user/corpora/evil/` (contains corrupted embeddings with NaNs or L2 norms > 50.0)
   Your tool must perfectly distinguish between the two corpora.
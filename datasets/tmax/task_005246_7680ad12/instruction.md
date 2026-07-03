You are an ML engineer preparing training data for machinery anomaly detection. We have an acoustic recording of a machine's operation in `/app/machinery_audio.wav`. 

You need to build a feature extraction pipeline and serve it via an HTTP API.

Part 1: Compilation
We provided a fast C++ spectral analysis utility in `/app/src/spectral/`. It depends on FFTW3. Compile this utility from source. The compiled binary should be placed at `/app/bin/spectral_extractor`. 

Part 2: Processing and Algorithmic Analysis
The raw audio contains periods of near-silence that cause our downstream Non-negative Matrix Factorization (NMF) to fail due to near-singular inputs. Write a Python script that uses the compiled `spectral_extractor` to convert `/app/machinery_audio.wav` into STFT magnitude windows.
Then, apply the following pipeline:
1. Compute the log-energy of each time window.
2. Perform Gaussian Kernel Density Estimation (KDE) on the log-energies to model the background noise distribution.
3. Identify the noise threshold at the 15th percentile of the estimated density and discard all windows with energy below this threshold to prevent matrix factorization on near-singular data.
4. Run a custom NMF algorithm on the remaining valid windows to extract exactly `k=3` components. You must implement a convergence test: the NMF iterations should halt when the Frobenius norm of the reconstruction error changes by less than `1e-5` between consecutive iterations.

Part 3: Multi-Protocol Serving
Create a Python HTTP server (e.g., using Flask or FastAPI) listening on `127.0.0.1:9090`. 
The server must implement a `GET /component/<int:window_idx>` endpoint. 
It should return a JSON response with the extracted NMF feature vector for the given *valid* window index (0-indexed based on the filtered list of windows). The JSON format must be: `{"window": <idx>, "features": [<float>, <float>, <float>]}`.
The server must also require a Bearer token for authentication. The token should be `SecretMLToken2024`. If the token is missing or invalid, return a 401 status code.

Start the server in the background so it can be queried. Create a file `/app/server_ready.txt` with the text "READY" once the server is actively listening.
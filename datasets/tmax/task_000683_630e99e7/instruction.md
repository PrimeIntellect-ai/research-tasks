As a machine learning engineer, I need you to set up a C++ based data processing service for our training pipeline. We have a corrupted matplotlib plot saved as an image, and we need to extract its underlying data to run some hypothesis testing and embedding generation.

Here is what you need to do:
1. There is an image file located at `/app/data_plot.png`. This image contains a series of numbers that were supposed to be plotted, but due to a backend misconfiguration, the plot is mostly blank with the raw data values printed as text on the image.
2. Use OCR (Tesseract is available on the system) to extract the numeric values from `/app/data_plot.png`.
3. Write a C++ program that computes a simple 1D "embedding" vector by normalizing these extracted numbers (z-score normalization: subtract the mean and divide by the standard deviation).
4. Your C++ program must act as an HTTP server listening on `127.0.0.1:8080`.
5. The server must expose a single endpoint: `GET /embedding`. When this endpoint is hit, it should return a JSON response containing the normalized numbers and the calculated mean and standard deviation.
   Example format: `{"mean": 10.5, "std": 2.1, "embedding": [-1.2, 0.5, 1.1]}`
6. Provide a bash script `/home/user/run_server.sh` that compiles your C++ code and starts the server. Make sure it stays running in the foreground or background so I can query it.

Please ensure your C++ server correctly handles the HTTP GET request and formats the JSON properly. You may use simple socket programming or any header-only library available in standard Linux package repositories (like `cpp-httplib` if you install it).
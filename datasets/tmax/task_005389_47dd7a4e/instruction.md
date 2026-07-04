You are a performance engineer building a test harness to validate the accuracy of a new numerical backend. You need to set up a microservice that validates matrix operations using statistical hypothesis testing.

Here are your instructions:
1. There is an image located at `/app/config.png` which contains a single line of text specifying a statistical threshold in the format: `ALPHA=<value>`. Extract this value (you can use tools like `tesseract`).
2. Write and start an HTTP server listening on `127.0.0.1:8080`.
3. The server must implement a single endpoint: `POST /test_svd`.
4. The `/test_svd` endpoint will receive a raw binary payload in the request body, which is a valid HDF5 file.
5. The HDF5 file will contain a single dataset at the root path named `"matrix"`.
6. For each request, your server must:
   - Read the 2D matrix from the HDF5 file.
   - Perform Singular Value Decomposition (SVD) on the matrix to extract the array of singular values.
   - Perform a 1-sample Kolmogorov-Smirnov (KS) test to compare the empirical distribution of these singular values against a continuous Uniform distribution over the interval [0, 1].
   - Compare the resulting p-value against the `ALPHA` value extracted from the image. If `p_value < ALPHA`, the null hypothesis is rejected.
7. The endpoint must return a JSON response with exactly this structure:
   `{"p_value": <float>, "reject": <bool>}`

Ensure your server runs in the background or foreground such that it remains active to serve requests. You may use any language or framework you prefer (e.g., Python with Flask/FastAPI, `h5py`, `numpy`, and `scipy`).
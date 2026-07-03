You are a machine learning engineer preparing a training pipeline. We have a proprietary text tokenization and embedding binary located at `/app/tokenizer_oracle`. This binary is stripped, but it acts as a black-box oracle: it reads a single line of text from standard input and prints exactly 20 space-separated floating-point numbers to standard output, representing the text's high-dimensional embedding.

Your task is to build a Go-based REST API that interfaces with this binary, applies dimensionality reduction, and tracks statistical metrics (specifically confidence intervals) across the dataset of processed requests.

Here are the exact specifications for the Go API:
1. **Environment Setup**: Create your project in `/home/user/data_api` and initialize a Go module named `data_api`.
2. **Server**: The Go HTTP server must listen on `127.0.0.1:9000`.
3. **Endpoint 1: POST `/process`**
   - **Input**: JSON payload `{"text": "your input string"}`
   - **Action**: 
     - Pass the `text` to the standard input of `/app/tokenizer_oracle` and capture the 20-dimensional float output.
     - Apply a simple dimensionality reduction: reduce the 20 dimensions down to 2 dimensions. The first reduced dimension ($D_1$) is the average of the first 10 original dimensions (indices 0-9). The second reduced dimension ($D_2$) is the average of the remaining 10 original dimensions (indices 10-19).
     - Store the reduced 2D vector in memory for statistical tracking.
   - **Output**: JSON payload `{"reduced_vector": [D1, D2]}`
4. **Endpoint 2: GET `/stats`**
   - **Action**: Compute the 95% confidence interval for the mean of the *first* reduced dimension ($D_1$) across all data points processed so far.
   - Use the sample standard deviation (Bessel's correction, dividing by $N-1$) and a Z-score of 1.96 for the 95% confidence level. If less than 2 points have been processed, return 0.0 for the mean and CI bounds.
   - **Output**: JSON payload exactly matching `{"mean_d1": <float>, "ci_lower": <float>, "ci_upper": <float>}`.

Ensure your Go application is robust, properly sets HTTP headers (`Content-Type: application/json`), and handles basic errors. Write the code, compile it, and leave the server running in the background.

Use only bash commands and standard Go libraries (no external third-party routing or math packages) to accomplish this.
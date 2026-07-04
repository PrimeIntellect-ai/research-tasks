You are a Data Engineer tasked with building an ETL pipeline and an inference API for a server monitoring system.

Your task consists of the following steps:

1. **Data Extraction (OCR):**
   There is an image located at `/app/data_table.png` which contains a printed CSV table of server metrics. The columns are `CPU,RAM,Disk,Network,Failure` (all continuous features except `Failure`, which is a binary 0/1 label).
   Use `tesseract` (which is pre-installed) to extract the text from this image and save it as a valid CSV file. Ensure you clean up any minor OCR artifacts so it parses correctly.

2. **Covariance Analysis:**
   Write a Go program at `/home/user/server.go` that reads the extracted CSV data.
   It must compute the sample covariance matrix (using $N-1$) for the four continuous features (`CPU`, `RAM`, `Disk`, `Network`) in that exact order.
   The program should write this $4 \times 4$ covariance matrix to `/home/user/covariance.txt`.
   Format requirements for `covariance.txt`:
   - 4 lines, each containing 4 comma-separated float values.
   - Each value must be formatted to exactly 4 decimal places (e.g., `123.4560`).

3. **Model Reconstruction:**
   Implement a logistic regression inference function in your Go program to predict the `Failure` label.
   Use the following pre-trained weights and bias:
   - $W_{CPU} = 0.05$
   - $W_{RAM} = 0.20$
   - $W_{Disk} = 0.01$
   - $W_{Network} = 0.001$
   - $Bias = -5.0$
   The probability of failure is $P = \frac{1}{1 + e^{-(W \cdot X + Bias)}}$.
   The predicted class is `1` if $P \ge 0.5$, otherwise `0`.

4. **API Serving:**
   Your Go program must start an HTTP server listening on `127.0.0.1:8080`.
   It must expose two endpoints:
   
   - `GET /accuracy`
     Calculates the classification accuracy of the reconstructed model on the entire extracted dataset (from the image).
     Returns JSON: `{"accuracy": <float>}` (e.g., `{"accuracy": 0.8}`)
     
   - `POST /predict`
     Accepts a JSON payload like: `{"CPU": 50.0, "RAM": 8.0, "Disk": 20.0, "Network": 100.0}`
     Returns the predicted probability and class as JSON: `{"probability": <float>, "class": <int>}`

5. **Security:**
   All HTTP requests to your server must include the header:
   `Authorization: Bearer secret-token-99`
   If the header is missing or incorrect, return a `401 Unauthorized` status.

6. **Execution:**
   Build and run your Go server in the background so that it is actively listening on port 8080 when you finish the task.
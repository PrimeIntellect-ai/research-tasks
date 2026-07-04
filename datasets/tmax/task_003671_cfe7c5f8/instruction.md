You are a build engineer managing numerical simulation artifacts. Recently, some artifact uploads have been poisoned with unstable simulation data. 

Your task is to build a robust validation pipeline consisting of an artifact scanner and a reverse proxy configuration to handle artifact upload traffic securely.

Step 1: Understand the Validation Metric
We have an architecture specification image located at `/app/spec.png`. Use an OCR tool (like `tesseract`) to read the hidden threshold parameter from this image. The validation algorithm you must implement is: 
1. Parse the input artifact file (which contains one floating-point number per line).
2. Calculate the "Instability Metric": the sum of the absolute differences between consecutive numbers in the file.
3. If the Instability Metric is strictly less than the threshold found in the image, the file is "clean". If it is greater than or equal to the threshold, it is "evil" (unstable).

Step 2: Create the Artifact Scanner
Write a Python CLI script at `/home/user/scanner.py` that takes a single file path as a command-line argument:
`python /home/user/scanner.py <path_to_artifact>`
- It should print "CLEAN" to standard output and exit with code 0 if the artifact is clean.
- It should print "EVIL" to standard output and exit with code 1 if the artifact is unstable.
Use virtual environments or standard package management as needed, but standard library is sufficient for the math.

Step 3: Test Against the Corpora
We have provided a sample of known artifacts:
- Clean artifacts are in `/app/corpora/clean/`
- Poisoned artifacts are in `/app/corpora/evil/`
Your scanner must successfully accept all clean files and reject all evil files. 

Step 4: Configure the Reverse Proxy
To protect the backend artifact storage service, create an Nginx configuration file at `/home/user/nginx.conf`. It must:
- Listen on port 8080.
- Proxy all requests to a backend service at `127.0.0.1:9000`.
- Implement request rate limiting, restricting clients to exactly 10 requests per second (using a shared memory zone named `upload_limit` of size 10m).

Ensure your Python script is executable and the Nginx configuration is syntactically valid. Do not start the Nginx server; simply provide the complete configuration file at the requested path.
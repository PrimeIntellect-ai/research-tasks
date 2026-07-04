You are a DevSecOps engineer responsible for enforcing policy as code. Our security architecture team has provided the new token signing policy seed in an image file located at `/app/policy_secret.png`. 

Your task is to:
1. Extract the text from the image file `/app/policy_secret.png`. The image contains a string in the format "POLICY_SEED: <SECRET_VALUE>". 
2. Write and run a Go-based HTTP authentication service that uses this `<SECRET_VALUE>` to generate and validate custom security tokens.
3. The service must listen on `127.0.0.1:8080`.
4. Implement two endpoints:
   - `POST /generate`: Accepts a JSON payload `{"user": "<username>"}`. It should return a JSON response `{"token": "<token>"}`. The token must be formatted as `<username>:<signature>`, where `<signature>` is the lowercase hex string of the SHA256 hash of the string `<username><SECRET_VALUE>`.
   - `POST /validate`: Accepts a JSON payload `{"token": "<token>"}`. It should recalculate the signature for the given username and compare it. It must return a JSON response `{"valid": true}` if the signature matches, or `{"valid": false}` otherwise.

Keep the server running in the background or foreground so that our automated policy enforcement checker can test the endpoints. Do not require any external database. Use standard Go libraries (e.g., `net/http`, `crypto/sha256`, `encoding/hex`, `encoding/json`).

Tesseract OCR (`tesseract`) is installed on the system to help you extract the text from the image.
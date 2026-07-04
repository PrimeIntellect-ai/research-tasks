You are an AI assistant helping a network engineer investigate a suspicious network dashboard capture. 

We have intercepted an image of an attacker's dashboard (`/app/dashboard.png`). The image contains an AES decryption key and an encrypted exploit payload that the attacker plans to use against our internal service running on `localhost` (port 8080).

Your task is to write a Bash script at `/home/user/analyze_traffic.sh` that automates the process of extracting the attacker's payload from an image, decrypting it, and testing it against our local service to see what information the attacker might compromise.

Your script must:
1. Accept an image file path as its first positional argument (e.g., `./analyze_traffic.sh /app/dashboard.png`).
2. Use Tesseract OCR to extract the text from the image.
3. Parse the extracted text to find the encryption key (look for the string `KEY: ` followed by a 32-character hex string) and the payload (look for `PAYLOAD: ` followed by a base64 encoded string).
4. Decrypt the payload using AES-128-ECB. The base64 string is the ciphertext. The 32-character hex string is the hex-encoded encryption key. No salt is used.
5. Send the decrypted payload via an HTTP POST request to `http://localhost:8080/vulnerable_endpoint` with the payload in the `query` field of a JSON body (e.g., `{"query": "<decrypted_payload>"}`). Make sure the content type is `application/json`.
6. Print the exact response body received from the server to standard output.

The service on port 8080 is already running. You can test your script against the provided `/app/dashboard.png` to ensure it works. 

Ensure your script is executable (`chmod +x /home/user/analyze_traffic.sh`). We will evaluate your script automatically on a hidden set of test images. Your score will be the fraction of tests where your script outputs the correct server response. You need an accuracy of 1.0 (100%) to pass.
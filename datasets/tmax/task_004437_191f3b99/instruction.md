You are an engineer tasked with porting an older, heavy image-processing tool into a lightweight, container-friendly microservice. The service needs to extract data from an image, decode it using a specific numerical algorithm, and serve the result over an HTTP REST API.

Here is the workflow you need to implement:

1. **OCR Processing**: An image containing encoded configuration data is located at `/app/data/config_scan.png`. You must use a tool like Tesseract (which is pre-installed) to extract the text from this image. The text consists of a single line of space-separated integers.

2. **Numerical Decoding via FFI**: The extracted integers represent coefficients of a polynomial evaluated at x=3, combined with a bitwise XOR key. You must write a C shared library (`/home/user/libdecoder.so`) containing a function with the following signature:
   `int decode_values(const int* input, int length, int x_val, int xor_key);`
   
   The algorithm for `decode_values` is:
   - Calculate the sum: `input[0]*x_val^0 + input[1]*x_val^1 + input[2]*x_val^2 + ... + input[length-1]*x_val^(length-1)`
   - Return the result XORed with `xor_key`.
   
   For this task, `x_val` is always 3, and `xor_key` is always 42. You must compile this C code into a shared library.

3. **REST API Construction**: Write a web server in any language of your choice (e.g., Python, Node.js, Go) that:
   - Listens on `127.0.0.1:8080`.
   - Exposes a `POST /api/v1/extract` endpoint.
   - Requires an `Authorization: Bearer dev-secret-token-99` header. If missing or incorrect, return a 401 Unauthorized status.
   - The POST request body will be JSON: `{"image_path": "/app/data/config_scan.png"}`.
   - The endpoint must read the specified image, perform OCR to get the integers, call your C library via FFI to decode them, and return a JSON response: `{"status": "success", "decoded_value": <integer>}`.
   - If the image path does not exist, return a 404 status.

Start your web server in the background and leave it running. You can create a script at `/home/user/start_server.sh` that launches your server. Do not exit until the server is running and listening on port 8080.
You are assisting a data researcher in automating dataset organization and validation. They have a legacy, closed-source schema validation tool located at `/app/validator`. This tool is a stripped, UPX-packed binary that acts as an oracle for data schema enforcement.

Your task is to build a microservice that validates incoming datasets and performs correlation/covariance analysis using linear algebra.

Here is what you need to do:
1. **Analyze the Oracle**: Reverse-engineer or test `/app/validator` to understand its expected input format (it reads from a file path passed as the first argument) and its exit codes. 
2. **Write a C++ Analyzer**: Create a C++ program at `/home/user/covar.cpp` (and compile it to `/home/user/covar`) that reads a valid, headerless CSV with 3 floating-point columns from standard input and computes the 3x3 **sample covariance matrix**.
   - The output must be exactly 3 lines.
   - Each line must contain 3 comma-separated floats, formatted to exactly 4 decimal places.
3. **Setup the Service**: Write a bash script `/home/user/start_service.sh` that uses standard CLI tools (like `nc` or `socat`) to listen on TCP port `8888`.
   - When a client connects, it will send a raw CSV string (ending with EOF).
   - The service must save this stream to a temporary file.
   - It must run `/app/validator <temp_file>`. 
   - If the validator exits with a success code (you must determine what this is), the service pipes the file content (ignoring headers if the validator requires them, though your C++ tool should process the numerical data) to your `/home/user/covar` binary, and sends the resulting covariance matrix back to the client.
   - If the validator rejects the schema, the service must send the exact string `ERR_SCHEMA` to the client.
   - The service must handle multiple sequential connections (one after another) and remain running.

Ensure your `start_service.sh` is executable and runs the service in the background or blocks appropriately.
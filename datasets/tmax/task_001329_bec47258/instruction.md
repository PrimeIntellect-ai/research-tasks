You are tasked with recovering and organizing a scattered microservices project. The previous developer was highly paranoid and stored the project's architectural configuration (file mapping and API reverse proxy routes) inside a lossless video file. 

Here is your multi-stage objective:

1. **Decode the Architecture from Video:**
   - There is a lossless video file located at `/app/secret_architecture.mp4`.
   - The configuration is a JSON string hidden in the video frames. 
   - For each frame $i$ (from $i=0$ to $N$), the Red channel value of the pixel at coordinate (x=0, y=0) corresponds directly to the ASCII integer code of the $i$-th character of the JSON string.
   - Extract the frames (e.g., using `ffmpeg` or `opencv-python`) and reconstruct the JSON string. 

2. **Organize Project Files:**
   - The decoded JSON will have a `file_mapping` key containing a dictionary where the keys are filenames currently residing in a flat directory `/home/user/messy_files/` and the values are the target relative paths where they should be moved within a new `/home/user/clean_project/` directory.
   - Create the necessary directory structure and move the files to their proper locations.

3. **Deploy the Reverse Proxy and APIs:**
   - The JSON string also contains a `routes` key mapping incoming path prefixes to backend microservice ports.
   - Start the backend microservices (the Python scripts you just organized into `/home/user/clean_project/backends/`) in the background. Each script takes a `--port` argument.
   - Write a FastAPI (or Flask/HTTP.server) reverse proxy in `/home/user/clean_project/proxy.py`.
   - The reverse proxy must run on port `8000`. It must dynamically route incoming REST requests to the correct backend service based on the `routes` configuration in the decoded JSON.
   - Ensure the proxy forwards HTTP methods (GET, POST), headers, and JSON bodies transparently.

4. **Package & Test:**
   - Create a virtual environment at `/home/user/venv`, install necessary dependencies (e.g., `fastapi`, `uvicorn`, `httpx`, `opencv-python`), and ensure your proxy server is running in the background.
   - Write a simple suite of unit/integration tests in `/home/user/clean_project/tests/test_proxy.py` to verify the proxy routes correctly. 

Complete the extraction, organization, and proxy deployment. Leave the proxy server running on port `8000` when you are finished.
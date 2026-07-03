We are setting up a data processing pipeline using Nginx, a Python Flask backend (managed by Gunicorn), and a custom data transformation script. However, the system is currently broken. When we send a request to the Nginx endpoint, we receive a 502 Bad Gateway error. Additionally, the core data transformation logic is missing its source code.

Your objectives are to fix the Nginx to Python backend connection, manage the containerized services/processes, and reverse-engineer and implement the missing data transformation script.

1. **Service Fixes**:
   - Nginx is configured to run as a local service using the configuration file at `/home/user/nginx/nginx.conf`, listening on port 8080.
   - The backend is a Flask app located at `/home/user/app/server.py`. It should be served via Gunicorn on a Unix socket.
   - Investigate the Nginx configuration and the Gunicorn startup process. Fix the 502 Bad Gateway error. The Nginx config is pointing to the wrong upstream Unix socket path, and the directory for the socket might have permission issues or not exist.
   - Ensure the Nginx and Gunicorn services are running and correctly communicating. Nginx must successfully proxy requests to the Flask app via the Unix socket.

2. **Recreate the Transformation Script**:
   - The Flask app shells out to a script at `/home/user/processor.py` to process POST request bodies. 
   - This script is currently missing. However, we have a compiled reference binary at `/app/oracle_processor` that performs the exact required logic.
   - Write a Python script at `/home/user/processor.py` that perfectly replicates the behavior of `/app/oracle_processor`. 
   - The program reads raw text from `stdin` (until EOF) and prints the transformed text to `stdout`.
   - You can execute `/app/oracle_processor` with various inputs to figure out its logic. Implement this logic in `/home/user/processor.py`.

Requirements:
- Your `/home/user/processor.py` must behave exactly like `/app/oracle_processor` for any arbitrary input.
- End-to-end requests: A POST request to `http://127.0.0.1:8080/process` with plain text data should successfully return the transformed data (processed by your script).
- Ensure all services are running in the background when you are finished.
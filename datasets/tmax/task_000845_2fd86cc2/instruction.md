You are helping a technical writer process and serve a batch of legacy manufacturing documentation. The system consists of a Python Flask backend and an Nginx reverse proxy, located in `/app/`. 

Your tasks are:

1. **Secure Nested Archive Extraction & Transformation**:
   There is an incoming nested archive at `/app/incoming/docs.tar`. Inside this tarball is a ZIP file named `payload.zip`. 
   Write a Python script at `/app/process_docs.py` that reads this nested archive and extracts the contents of `payload.zip` into the directory `/app/extracted/`. 
   **Security Warning:** The ZIP file was created by an untrusted source and contains a "Zip Slip" directory traversal attack (a file with a `../` path attempting to overwrite `/app/system_config.txt`). Your extraction logic MUST ignore or sanitize any files that attempt to extract outside of `/app/extracted/`.
   
2. **Format Parsing & Text Transformation**:
   The extracted text files contain embedded 3D printer GCode snippets wrapped in `[GCODE]` and `[/GCODE]` tags. Modify the extracted `.txt` files in place (using Python, `sed`, or `awk`) to transform specific GCode commands:
   Find any line containing `G1 X<number> Y<number>` inside these blocks and transform it into the format `LINEAR_MOVE X:<number> Y:<number>`. Leave other text unchanged.

3. **Multi-Service Integration**:
   The documentation needs to be served via a Flask/Nginx stack. 
   - Edit the Nginx configuration at `/app/nginx.conf`. Ensure it listens on port `8080` (as a non-root user) and proxies requests from the `/docs/` path to the Flask app.
   - Edit the Flask application at `/app/app.py`. Configure it to run on `127.0.0.1:5000` and serve the raw text content of the files in `/app/extracted/` when a `GET` request is made to `/docs/<filename>`.
   - Start the services using the provided `/app/start.sh` script.

Verify your work by ensuring `curl http://127.0.0.1:8080/docs/doc1.txt` returns the successfully transformed documentation. Ensure `/app/system_config.txt` remains unaltered.
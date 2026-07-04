You are a web developer building a new feature for an image processing service. The service dynamically loads shared libraries (plugins) specified via a JSON configuration. To ensure system security and stability, we need a payload validator and a reverse proxy configuration.

Your tasks are:

1. **Extract Configuration**: 
   There is an image file located at `/app/config_spec.png`. It contains two key configuration values: a proxy port and an allowed plugin directory. Use OCR (e.g., `tesseract`) to extract these values.

2. **Reverse Proxy Configuration**:
   Write an Nginx configuration file at `/home/user/nginx.conf`. This configuration should set up a server listening on port 80, which reverse-proxies all requests (`/`) to `http://127.0.0.1:<PROXY_PORT>`, where `<PROXY_PORT>` is the port number extracted from the image.

3. **Adversarial Payload Sanitiser (Rust)**:
   Create a Rust CLI project in `/home/user/sanitiser`. When built, the binary should be executable as `cargo run -- <path_to_json_file>`. 
   
   The JSON file represents a processing pipeline and has the following structure:
   ```json
   {
     "pipeline": [
       {
         "step_id": "step1",
         "plugin_path": "/var/lib/plugins/libresize.so",
         "depends_on": []
       },
       {
         "step_id": "step2",
         "plugin_path": "/var/lib/plugins/libgray.so",
         "depends_on": ["step1"]
       }
     ]
   }
   ```
   
   Your Rust program must validate the JSON and exit with code `0` if it is valid (clean) and code `1` if it is invalid (evil).
   A payload is **invalid (evil)** if EITHER of the following conditions is met:
   - **Dependency Cycle**: The `depends_on` relationships form a cycle (the pipeline graph must be a Directed Acyclic Graph).
   - **Unauthorized Shared Library**: Any `plugin_path` does not start exactly with the allowed plugin directory string extracted from the image.

Build your Rust project so that the verifier can test it. The automated test suite will run your binary against two corpora of JSON files: a "clean" corpus and an "evil" corpus.
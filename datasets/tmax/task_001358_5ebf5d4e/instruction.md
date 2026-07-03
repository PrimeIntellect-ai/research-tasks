You are tasked with recovering Kubernetes manifests that were incorrectly dumped into a log file by a broken operator cron job, and then securely exposing them for another service to ingest.

The cron job failed due to a missing binary in its `PATH`, so instead of applying the manifests, it dumped the raw template output into a log file at `/home/user/operator/cron_out.log`.

Perform the following steps:

1. **Extract Manifests**: Process the file `/home/user/operator/cron_out.log`. Extract all text that occurs strictly between the lines `RAW_MANIFEST_START` and `RAW_MANIFEST_END`. 
2. **Save Recovered Files**: Create an idempotent Python script or use shell text processing pipelines to save each extracted manifest as an individual file in the directory `/home/user/operator/recovered/` (create this directory if it does not exist). Name the files sequentially starting from 0: `manifest_0.yaml`, `manifest_1.yaml`, etc.
3. **Secure Web Server**: Write a robust Python script at `/home/user/operator/serve.py` that starts an HTTPS server on `0.0.0.0` port `8443`. 
    * The server must serve the contents of the `/home/user/operator/recovered/` directory.
    * Use the provided TLS certificate `/home/user/operator/cert.pem` and private key `/home/user/operator/key.pem` to secure the server.
4. **Execution**: Run your `serve.py` script in the background so that it remains active.

Ensure the extracted YAML files do not contain the `RAW_MANIFEST_START` or `RAW_MANIFEST_END` boundary lines, and preserve the original indentation.
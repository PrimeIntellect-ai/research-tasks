As a cloud architect migrating legacy services, you must reconstruct our core data processing pipeline. The original source code and configuration files were lost during a datacenter outage. 

1. **Configuration Recovery:** A screenshot of the original configuration terminal survives at `/app/legacy_config.png`. Use OCR tools (like `tesseract`, which is installed) to extract the secret `XOR_KEY` and `MOD_FACTOR` values from this image.
2. **C++ Implementation:** Recreate the processor logic. Write a C++ program at `/home/user/migrated_processor.cpp` and compile it to `/home/user/migrated_processor`. It must accept a single command-line argument (an alphanumeric string). For each character, it must apply an XOR operation with the extracted `XOR_KEY`, add the `MOD_FACTOR`, and output the resulting integer values space-separated. Your implementation must perfectly match the behavior of the surviving, stripped legacy binary.
3. **Deployment & Process Control:** Write a deployment script `/home/user/deploy.sh` (make it executable). The script must:
   - Establish a background SSH local port forwarding tunnel mapping localhost:8080 to localhost:9090.
   - Launch a background monitoring loop that continuously checks if a dummy service `python3 -m http.server 9090` is running. If not, it starts it.
   - Perform a health check every 5 seconds, writing the timestamp and status to `/home/user/health.log`.

Ensure all files are created exactly at the specified paths. The automated verification will test your C++ binary against thousands of inputs to ensure exact equivalence with the legacy system, and will verify your deployment script's tunneling and monitoring capabilities.
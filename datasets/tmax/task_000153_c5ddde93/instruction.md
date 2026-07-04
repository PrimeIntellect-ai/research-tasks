You are a platform engineer maintaining the CI/CD pipeline for a web security company. Recently, our lightning-fast Rust-based Web Application Firewall (WAF) routing component started failing to compile in the pipeline due to complex lifetime issues introduced in a recent PR. To keep the pipeline green while the systems team fixes the Rust WAF, we need you to build a Python-based mock WAF tester that implements the exact same routing and parameter parsing state machine.

We have an architectural diagram of the WAF routing rules exported as an image at `/app/waf_rules.png`. You need to extract the routing logic and state machine from this image and implement it in Python.

Your task:
1. **Analyze the WAF Rules:** Use OCR or visual analysis to read `/app/waf_rules.png`. It describes a state machine for URL routing and query parameter validation.
2. **Implement the WAF:** Write a Python script at `/home/user/waf_tester.py` that parses URLs, routes them according to the rules, and enforces the security checks. 
3. **Process the Pipeline Data:** You are provided with a test fixture of incoming HTTP requests at `/app/requests.json`. Each entry contains a `path` and `query_params`.
4. **Generate Predictions:** Your script must evaluate each request in `/app/requests.json` using your implemented WAF state machine. Output the results to `/home/user/predictions.json`.
    * The output format must be a JSON array of strings, where each string is either `"ALLOW"` or `"BLOCK"`, corresponding sequentially to the requests in `/app/requests.json`.
5. **Testing and Accuracy:** Your implementation must be highly accurate. The pipeline verification step will compare your `/home/user/predictions.json` against a hidden ground-truth dataset. 

**Constraints:**
- The primary language must be Python.
- You must create the WAF logic from scratch based on the provided image diagram.
- `tesseract-ocr` is installed and available if you need to extract text from the image.
- Ensure your script is efficient; it should process the requests quickly.

Fix the pipeline by providing the accurate `/home/user/predictions.json`.
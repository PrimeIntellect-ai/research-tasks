You are an AI assistant acting as a FinOps analyst. Your goal is to optimize cloud costs by enforcing deployment policies, and to set up a secure local dashboard for approved configurations.

You need to complete the following multi-stage workflow:

1. **Extract Policy Limits:**
   There is a monthly invoice summary image located at `/app/invoice_summary.png`. Use OCR (e.g., `tesseract`, which is preinstalled) to read it. The image contains text specifying the "APPROVED_FAMILIES" (a list of allowed AWS instance families, e.g., "t3, m5") and the "MAX_DEPLOYMENT_COST" (an integer dollar amount).

2. **Develop a FinOps Filter:**
   Write a Python script at `/home/user/finops_filter.py` that takes a single file path as a command-line argument. The file will be a JSON deployment configuration containing an array of instances. Example:
   ```json
   {
     "app_name": "api-service",
     "instances": [
       {"type": "t3.medium", "count": 4, "monthly_cost_per_unit": 30},
       {"type": "x1.32xlarge", "count": 1, "monthly_cost_per_unit": 3000}
     ]
   }
   ```
   The script must enforce the policies extracted from the image:
   - Every instance `type` must start with one of the `APPROVED_FAMILIES` (e.g., if "t3" is approved, "t3.medium" is allowed).
   - The total monthly cost (sum of `count * monthly_cost_per_unit` across all instances) must be less than or equal to `MAX_DEPLOYMENT_COST`.
   
   If the configuration passes ALL checks, the script must exit with code `0`. If it violates ANY policy, the script must exit with code `1`.

3. **Secure Web Dashboard & Staged Deployments:**
   - Configure and start an `nginx` web server listening on port `8443` with a self-signed TLS certificate. The document root should be `/home/user/www`.
   - Write an idempotent Bash script at `/home/user/deploy.sh` that takes a JSON configuration file as an argument. 
   - The script should run `finops_filter.py` on the file.
   - If the filter rejects the config, the script should abort.
   - If approved, it should create a directory `/home/user/www/<app_name>-<timestamp>` (using the `app_name` from the JSON), copy the JSON file into it as `config.json`, and update a symlink at `/home/user/www/<app_name>-live` to point to this new directory (facilitating a rolling deployment structure).

Ensure your `finops_filter.py` is robust, as it will be tested against a hidden corpus of clean and wasteful configurations.
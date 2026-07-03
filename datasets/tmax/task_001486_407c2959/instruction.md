You are tasked with securing and repairing a configuration management ingestion pipeline. The system runs three cooperating services that are brought up automatically by our environment startup script `/app/start_services.sh`:
1. Nginx (Reverse Proxy) listening on port 8080.
2. A Python Flask API (Configuration Ingestor) listening on port 5000.
3. A Redis instance (State Cache) listening on port 6379.

Currently, configuration bundles (which are `.tar.gz` files containing JSON files) are uploaded via Nginx, but the Flask API is blindly extracting them and loading them into Redis. This is a severe security risk. Furthermore, the system is supposed to convert `app_config.json` files into an XML format before caching, but this is currently broken.

Your task is divided into two parts:

**Part 1: Build the Configuration Sanitizer & Converter**
Write a Bash script at `/home/user/pipeline/sanitizer.sh` that takes exactly two arguments: the path to an input `.tar.gz` configuration bundle, and an output directory path.
The script must:
1. Safely extract the archive into a temporary working directory.
2. Reject the archive (exit with code 1 and print "REJECTED") if it contains:
   - Any symbolic links pointing outside the extraction directory or absolute paths.
   - Any hard links.
   - Any files with the `.sh` extension (malicious payload attempt).
3. If the archive is safe, find any file named `app_config.json` (there may be multiple in different subdirectories). Parse the JSON and convert it to a simple XML format. For example, `{"service": "web", "workers": 4}` must become `<config><service>web</service><workers>4</workers></config>`. Save the converted file as `app_config.xml` in the exact same subdirectory, and delete the original `app_config.json`.
4. Pack the safe, converted files into a new `.tar.gz` archive, placing it in the specified output directory and naming it `sanitized_bundle.tar.gz`. Exit with code 0 and print "ACCEPTED".

Your script will be tested against two sets of corpora:
- `/home/user/corpora/clean/`: Contains 50 valid configuration bundles. Your script must ACCEPT 100% of these.
- `/home/user/corpora/evil/`: Contains 50 malicious bundles (directory traversal symlinks, hardlinks to `/etc/shadow`, embedded shell scripts). Your script must REJECT 100% of these.

**Part 2: Fix the Multi-Service Pipeline**
1. Reconfigure the Nginx service. Its config file at `/home/user/services/nginx/nginx.conf` has a typo and is proxying `/upload` to port 5001 instead of the Flask app's port 5000. Fix it and reload Nginx.
2. Edit the Flask application at `/home/user/services/flask/app.py`. Modify the `/upload` endpoint so that, instead of extracting files directly using Python, it shells out to your `/home/user/pipeline/sanitizer.sh`. It should pass the uploaded file and a safe temporary output directory.
3. If the script succeeds ("ACCEPTED"), the Flask app must parse the resulting `app_config.xml` files inside `sanitized_bundle.tar.gz` and write a key to Redis: `SET config_status "SECURE_UPDATE_APPLIED"`.
4. Ensure the end-to-end flow works. You can test it by running `curl -F "file=@/home/user/corpora/clean/test1.tar.gz" http://localhost:8080/upload`.

Do not change the ports of the existing services. Ensure your Bash script `/home/user/pipeline/sanitizer.sh` is executable.
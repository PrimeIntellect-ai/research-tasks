You are an infrastructure engineer automating the provisioning of a custom Web Application Firewall (WAF) script for our web servers. 

We recently received a security bulletin as an image file located at `/app/waf_rules.png`. You must extract the text from this image (you can use `tesseract`) to determine the exact malicious patterns we need to block. The image contains a specific User-Agent string and a specific URI path that are considered dangerous.

Your primary objective is to write a classifier script that can accurately distinguish between safe and malicious HTTP requests based on the rules extracted from the image.

Here are your tasks:
1. Read `/app/waf_rules.png` to find the exact "Malicious User-Agent" and "Restricted URI Path".
2. Create an executable script at `/home/user/classifier.sh` (you may write it in Bash, Python, or any other language of your choice, but the entry point must be this shell script).
3. The script `/home/user/classifier.sh` will be invoked with a single argument: the absolute path to a file containing a raw HTTP request.
4. Your script must read the file and determine if it is malicious:
   - If the request contains the malicious User-Agent OR requests the restricted URI path, the script must exit with status code `1` (reject).
   - If the request does not contain either of the malicious patterns, the script must exit with status code `0` (accept).

Additionally, to prepare the infrastructure for testing, you must:
5. Create a dummy network interface named `waf0` and assign it the IP address `10.100.0.1/24`.
6. Generate a self-signed TLS certificate and private key at `/home/user/certs/tls.crt` and `/home/user/certs/tls.key`.

Ensure your `classifier.sh` script is highly accurate. It will be tested against a large corpus of clean and malicious requests. False positives (rejecting a clean request) and false negatives (accepting an evil request) are not acceptable.
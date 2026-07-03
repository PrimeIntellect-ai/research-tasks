You are a log analyst investigating suspicious activity in your system's audit logs. Recently, you discovered a logging pipeline that silently drops rows containing embedded newlines, which attackers are exploiting to hide their tracks. 

To prevent this, you need to write a robust log classifier. The corporate logging policy and validation rules have been provided to you as an image file located at `/app/policy.png`. 

Your task:
1. Extract the validation rules from `/app/policy.png`.
2. Write a Python script at `/home/user/log_classifier.py` that takes a single command-line argument (the path to a CSV file).
3. The script must read the CSV, reshape it, clean it, and evaluate it strictly according to the rules found in the image.
4. If the CSV file violates ANY of the rejection criteria in the policy, your script must exit with status code `1` (indicating a malicious/malformed file).
5. If the CSV file passes all checks, your script must exit with status code `0` (indicating a clean file).

Ensure your script handles standard CSV parsing securely. You are free to use standard Python libraries or install packages like `pandas` if needed.
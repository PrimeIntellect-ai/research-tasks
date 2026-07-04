I need you to create a configuration validator script for our tracking system. We have a set of configuration files, but some of them have been tampered with or misconfigured. 

Please write a Python script at `/app/verify_config.py` that takes a single file path as an argument and exits with code `0` if the configuration is valid (clean), and code `1` if it is invalid (evil).

To determine the validation rules:
1. Extract the nested archive at `/app/config_templates.tar.gz`. Deep inside this archive, you will find a CSV file containing the list of perfectly allowed configuration keys. A valid configuration must ONLY contain keys present in this CSV.
2. We have a physical policy document that was scanned. Run OCR (using `tesseract`) on the image at `/app/policy.png`. The image contains a single word which represents a mandatory "environment_id" value. A valid configuration MUST have this exact string as the value for the `environment_id` key.
3. Security constraint: Invalid configurations sometimes use symbolic links to point to sensitive system files. If the provided file is a symbolic link, it must be rejected.
4. The configurations are in JSON format. 

Your script will be tested against two hidden directories containing valid and invalid configurations. Ensure your script only uses standard libraries and exits with the correct status code.
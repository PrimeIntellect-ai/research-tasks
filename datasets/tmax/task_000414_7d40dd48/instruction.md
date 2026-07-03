You are a container specialist managing a suite of microservices. We are setting up a secure automated backup and log rotation system for these services. 

The legacy authentication system for our backup vault uses a custom token generation algorithm. The documentation for this algorithm was lost during a recent migration, but we managed to recover a screenshot of the original specification.

The screenshot is located at `/app/token_rules.png`. 

Your task is to:
1. Extract the token generation rules from the image (the `tesseract` OCR package is preinstalled).
2. Write a Python script at `/home/user/generate_token.py` that implements the exact logic specified in the image.

The script must accept exactly two command-line arguments in this order:
1. `SERVICE_NAME` (a string containing alphanumeric characters)
2. `TIMESTAMP` (an integer)

The script must print ONLY the generated token string to standard output. It must be executable (`chmod +x`). Ensure your script handles the input arguments properly and strictly follows the extracted rules, as it will be rigorously tested against thousands of randomized inputs to ensure perfect backward compatibility.
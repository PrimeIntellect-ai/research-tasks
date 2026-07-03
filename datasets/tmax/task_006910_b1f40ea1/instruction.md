You are an operations engineer triaging an incident involving a critical mathematical service. The service computes the numerical integration (using the Trapezoidal rule) of a dataset containing sensor readings.

The service directory is located at `/home/user/math_service`.
However, the service is currently failing to produce the correct results due to several issues:
1. The input data file `data.enc` is XOR-encrypted. The decryption key was accidentally committed to the git repository in the past and subsequently removed. You must find this key to decrypt the data.
2. The decrypted data contains occasional corrupted, non-numeric lines (e.g., network artifacts) which cause the script to crash. The script must be updated to gracefully skip these corrupted lines and only process valid numeric values.
3. The core integration algorithm in `integrate.py` contains an off-by-one boundary error, leading to an incorrect mathematical result because it does not process the entire valid dataset.

Your task:
1. Perform git forensics in `/home/user/math_service` to recover the numeric XOR key.
2. Fix `integrate.py` so that it correctly handles corrupted input (by skipping non-numeric lines) and correctly calculates the integral over the entire valid dataset without missing any intervals.
3. Run the fixed script using the encrypted data file and the recovered key: `python3 integrate.py data.enc <RECOVERED_KEY>`
4. Save the final numerical output of the script to `/home/user/math_service/result.txt`. The file should contain only the final computed floating-point value.
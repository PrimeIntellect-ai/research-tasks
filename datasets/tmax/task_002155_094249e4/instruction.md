You are an on-call systems engineer. You have just been paged at 3:00 AM. 

Alert: The legacy payload ingestion pipeline has failed. The service crashed, leaving a corrupted environment, and the backup Python processor is producing statistically anomalous outputs. 

Your tasks:
1. Diagnose the Environment Misconfiguration: The last known working configuration was captured in a server console screenshot before the KVM crashed. This image is located at `/app/console_panic.png`. Extract the required configuration offset value from this image (you may use `tesseract` or similar tools).
2. Fix the Processing Script: The current buggy Python processor at `/home/user/processor.py` fails on certain inputs and miscalculates the payload transformations. Use interactive debugging and stack trace analysis to find why it is dropping bytes and applying the wrong bitwise operations.
3. Integrate the Config and Fix: Create a final Python script at `/home/user/solution.py`. This script must act as a drop-in replacement for the ingestion service. 

Requirements for `/home/user/solution.py`:
- It must accept a single command-line argument: a raw hexadecimal string (e.g., `A1B2C3`).
- It must read the environment variable `INGESTION_OFFSET` (which you must set in your shell based on the value found in the screenshot).
- It must output strictly the processed hexadecimal string to `stdout`.
- The output must be bit-exact to the legacy C-based oracle. 

Ensure your final script correctly handles all edge cases and runs smoothly. Automated systems will verify your script by fuzzing it against thousands of payloads.
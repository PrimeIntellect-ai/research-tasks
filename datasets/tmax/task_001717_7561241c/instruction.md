You are an operations engineer tasked with triaging an incident. A mathematical processing service, `math_service.py`, has been crashing periodically in production. We managed to capture a memory dump of the process right after a crash, saved at `/home/user/process.dmp`.

The service accepts inputs via command line arguments. The inputs are base64-encoded, zlib-compressed JSON objects containing mathematical matrices. Somewhere in the memory dump is the exact payload that caused the crash, along with several other valid payloads that were in memory at the time.

Your task is to:
1. Extract the readable strings from the memory dump `/home/user/process.dmp`.
2. Identify strings that could be valid base64-encoded payloads for the service.
3. Write a short script or command loop to "fuzz" or test the `/home/user/math_service.py` script with the extracted payloads to see which one causes an `AssertionError`.
4. Once identified, save the EXACT base64 string of the crashing payload to `/home/user/crashing_payload.txt`.
5. Save the exact text of the AssertionError message to `/home/user/error_msg.txt`.

Ensure your output files do not contain extra whitespace or newlines beyond the requested content.
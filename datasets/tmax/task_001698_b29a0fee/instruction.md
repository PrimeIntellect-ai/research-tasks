You are a security researcher analyzing a failure in a data processing container. 

A Python service recently crashed when attempting to process a specific binary packet. You have been provided with the service logs and the parsing script that failed. 

Your objectives are:
1. Inspect `/home/user/service.log` to find the base64-encoded payload that caused the crash.
2. Analyze the provided parser script `/home/user/parse_packet.py`. The script attempts to find a magic header and read a 4-byte offset to locate a string. However, it fails to parse the crash payload properly due to a format parsing bug involving integer representation.
3. Fix `parse_packet.py` so that it correctly handles the binary format (specifically, handling the relative offset properly).
4. Run your fixed script on the decoded binary payload to extract the hidden string.
5. Save the extracted string to `/home/user/flag.txt`.

Ensure the extracted string is saved exactly as it is decoded, with no extraneous newlines or characters.
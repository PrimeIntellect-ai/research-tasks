I am migrating a legacy data processing pipeline from Python 2 to Python 3, but I'm hitting some serialization and dependency issues. 

There is a Python script at `/home/user/ws_processor.py` that reads a JSON file from `/home/user/data.json`, serializes it, calculates a CRC32 checksum, and sends the payload via WebSockets to a local server. In Python 2, this worked fine, but in Python 3 it crashes with a `TypeError` because the checksum function expects bytes, not strings.

Your task is to:
1. Fix the string/bytes serialization issue in `/home/user/ws_processor.py` so it is compatible with Python 3.
2. Create a Python 3 virtual environment at `/home/user/venv`.
3. Install the `websockets` package inside this virtual environment.
4. Start the provided WebSocket echo server located at `/home/user/echo_server.py` in the background (using the virtual environment).
5. Run the fixed `/home/user/ws_processor.py` script.

When successful, `ws_processor.py` will receive the echoed response from the server and automatically write it to `/home/user/success.log`. 

Ensure that the final output in `/home/user/success.log` is generated correctly. Do not modify `/home/user/data.json` or `/home/user/echo_server.py`.
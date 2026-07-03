I need you to modernize a legacy Python 2 mathematical encoding service located at `/app/legacy_service`. 

The service has several major issues:
1. **Circular Imports:** The codebase has a nasty circular import between `server.py`, `router.py`, and `math_utils.py` which prevents the server from building or importing cleanly. The previous developer used inline import hacks to make it barely run.
2. **Python 2 Legacy:** It uses Python 2 standard libraries (`BaseHTTPServer`, `urlparse`) and handles strings as raw bytes, which completely breaks when handling non-ASCII text.
3. **Buggy Math Logic:** The Python checksum logic in `math_utils.py` computes an incorrect checksum for multibyte characters. 

I have provided a compiled reference binary at `/app/reference_oracle`. This stripped binary represents the exact, correct mathematical checksum algorithm we must use. If you execute `/app/reference_oracle "some text"`, it will print the correct integer checksum to standard output.

Your objectives:
1. **Refactor & Migrate:** Fix the circular dependencies and cleanly migrate the codebase to Python 3. You may use the Python 3 standard library `http.server` and `urllib.parse`.
2. **Fix the Encoding/Math:** Update the checksum generation so it exactly matches the output of `/app/reference_oracle` for any string, including complex UTF-8 characters. You can either reverse-engineer the algorithm from the oracle (it is a relatively simple arithmetic hash over the encoded bytes) or wrap the oracle executable via `subprocess`.
3. **Run the API:** Start your modernized Python 3 server on `127.0.0.1:8080` and leave it running in the background.

The API must expose a single HTTP GET endpoint:
`GET /compute?text=<URL_ENCODED_STRING>`

It must parse the `text` parameter and return an HTTP 200 response with a JSON body in the exact format:
`{"hash": <integer>}`

Ensure your server is robust and properly handles URL encoded data. Leave the server running as your final step.
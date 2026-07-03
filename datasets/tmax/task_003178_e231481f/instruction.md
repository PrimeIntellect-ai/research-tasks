I need you to help me migrate an old Python 2 data processing pipeline to Python 3 and fix a CI import ordering issue. 

Here is the situation:
1. We have a legacy Python 2 script at `/app/legacy_processor.py` that interfaces with a compiled shared library `/app/libdata.so` using `ctypes`. The old code fails in Python 3 due to standard library changes (e.g., `urllib2`, `BaseHTTPServer`) and ABI issues (Python 3 strings vs bytes when passing arguments to the C library).
2. The CI pipeline is also failing because the internal modules must be initialized in a specific order with specific semantic versions, but the documentation was lost. Luckily, I found an old screenshot of the architecture diagram at `/app/legacy_specs.png`.
3. You need to read `/app/legacy_specs.png` (using OCR/tesseract) to figure out the exact initialization order and the semantic versions of the three core modules (`Auth`, `Data`, `Sink`).
4. Migrate `/app/legacy_processor.py` to Python 3. Fix the `ctypes` struct definitions to properly handle the ABI (ensuring C-strings are passed as bytes).
5. Modify the script to implement a simple REST API (using Python 3's `http.server`). It should listen on port `8080`.
6. When a `GET /config` request is made to the API, it must return a JSON array of the modules in the exact initialization order specified in the image, along with their parsed semantic versions. Example format: `[{"module": "Auth", "version": "1.2.0"}, ...]`.
7. Write the same JSON array to `/app/final_config.json`.

Please complete the migration, start the server in the background, and create the `/app/final_config.json` file.
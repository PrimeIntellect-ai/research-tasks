I am building a data processing service where a Python API delegates heavy array sorting and diffing to a high-performance C library. Unfortunately, my C project is currently failing to link properly, and the server configuration was given to me as a screenshot that I can't copy-paste from. 

Please fix the system and bring up the server.

Here is what you need to do:

1. **Extract Configuration:** There is an image file located at `/app/server_config.png`. It contains two lines of text specifying the port the server must listen on and the authentication token. Use OCR (e.g., `tesseract`) to read it. The text format is:
   `PORT=<port_number>`
   `TOKEN=<auth_token>`

2. **Fix the C Library:** 
   In `/home/user/clib/`, there is a C project containing `sorter.c`, `sorter.h`, and a `Makefile`. 
   The Makefile is broken—it fails to properly compile and link the code into a shared library (`libsorter.so`) due to missing compiler flags for shared libraries and Position Independent Code. 
   Fix the `Makefile` and run `make` so that `libsorter.so` is successfully built in `/home/user/clib/`.

3. **Complete and Run the Python API:**
   In `/home/user/server.py`, there is a partially written Python Flask/FastAPI (or simple HTTP) server. You need to:
   - Make it listen on the port extracted from the image on `127.0.0.1`.
   - Implement an HTTP `POST` endpoint at `/api/v1/process`.
   - The endpoint must require an `Authorization: Bearer <auth_token>` header, using the token extracted from the image. If missing or incorrect, return a 401 status code.
   - The endpoint will receive a JSON payload: `{"arrays": [[3, 1, 2], [9, 5, 6]]}` (a list of integer lists).
   - The Python code must parse this, merge all the sub-arrays into a single flat list, use `ctypes` to pass this merged list to the `sort_array` function in `libsorter.so`, and return a JSON response with the sorted array: `{"result": [1, 2, 3, 5, 6, 9]}`.

Start the server process in the background or leave it running in the terminal so my automated tests can send HTTP requests to it.
You are acting as an AI assistant helping a technical writer modernize and serve a legacy documentation archive.

Your task has three main phases: Archive Processing, OCR, and Service Deployment.

**1. Archive Processing & Text Editing**
You have a compressed documentation archive located at `/app/docs.tar.gz`. 
Extract it into `/app/docs/`. 
Inside, you will find several `.txt` files. You must perform a large-scale text edit on all `.txt` files in this directory:
- Replace all instances of the string `v1.0` with `v2.0`.
- Prepend the exact string `[INTERNAL DRAFT]\n` to the very beginning of every `.txt` file.

**2. Image OCR**
There is a legacy architecture diagram located at `/app/diagram.png`.
Extract the text from this image using `tesseract` and save it to `/app/docs/diagram.txt`. Prepend `[INTERNAL DRAFT]\n` to this text file as well.

**3. C++ HTTP Documentation Server**
Write and compile a C++ HTTP server (you may use raw sockets, `Boost.Asio`, `libmicrohttpd`, or any other C++ library you wish to install).
The server must listen on `127.0.0.1:8080`.

It must read a configuration file located at `/app/route_config.txt`. Each line of this file contains a route mapping in the format: `ROUTE=FILE_PATH` (e.g., `/intro=/app/docs/intro.txt`).
For every GET request to a defined `ROUTE`, the server must read the corresponding `FILE_PATH` and serve its contents with an HTTP 200 OK status and `Content-Type: text/plain`.
If a requested route is not in the configuration file, return HTTP 404 Not Found.

Compile your server, start it in the background, and ensure it is listening on port 8080 before completing your turn.

Files to expect on the system:
- `/app/docs.tar.gz`
- `/app/diagram.png`
- `/app/route_config.txt`
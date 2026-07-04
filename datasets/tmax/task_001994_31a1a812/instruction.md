You are tasked with fixing a broken C++ mathematical microservice, completing its implementation based on a visual specification, and deploying it locally behind a reverse proxy.

The microservice is located in `/home/user/math_service`. It is meant to expose a REST API that computes a specific mathematical function. However, the project currently fails to build due to linking errors, and the core mathematical logic is missing.

Here are your steps:
1. **Extract Mathematical Parameters:** There is an image at `/app/coefficients.png`. It contains the specific parameters (A, B, and C) for the equation you need to implement: `f(x) = A * sin(x) + B * cos(x) + C * x^2`. Use a tool like `tesseract` to read these values.
2. **Fix the Build System:** The `Makefile` in `/home/user/math_service` fails to compile the `server` executable. The linking stage is broken due to incorrect library order and missing flags required by the `httplib.h` header. Diagnose and fix the `Makefile` so that `make` successfully produces the `server` executable.
3. **Implement the API:** Complete the C++ code in `/home/user/math_service/server.cpp`. It uses the `httplib` library to run an HTTP server on port `9090`. You must implement a `POST /compute` endpoint. The endpoint should accept a JSON payload in the format `{"x": 2.5}` and return a JSON payload `{"result": <computed_value>}` using the equation and coefficients you extracted in step 1.
4. **Configure Reverse Proxy:** Write an Nginx configuration file at `/home/user/proxy/nginx.conf`. It must listen on `127.0.0.1:8080` and proxy all requests to your C++ API on `127.0.0.1:9090`. Ensure the config is self-contained so Nginx can run entirely within `/home/user/proxy` without root access (e.g., place `pid`, `error_log`, and `access_log` in `/home/user/proxy/`).
5. **Start the Services:** 
   - Start your C++ microservice (`/home/user/math_service/server`).
   - Start the reverse proxy using: `nginx -c /home/user/proxy/nginx.conf -p /home/user/proxy/`

A background verifier will continuously check the API through the reverse proxy (port `8080`). It will send a series of values for `x` and calculate the Mean Squared Error (MSE) of your API's responses against the theoretical exact values. You must achieve an MSE of less than `0.001` to pass. Leave the server and proxy running when you are finished.
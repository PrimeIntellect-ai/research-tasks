You are a data engineer building an end-to-end ETL pipeline and inference server in C. 

Your workspace contains:
1. A dataset at `/home/user/data.csv` (100 rows, header: `X,Y`). The first 80 rows are the training set, and the last 20 rows are the test set.
2. A training program at `/home/user/train.c`. This program implements a simple linear regression using Gradient Descent. Currently, it normalizes the features (`X`) by calculating the minimum and maximum values over the *entire* 100-row dataset before splitting it. This is a data leakage bug! The scaling parameters (min and max) must be calculated *only* on the training set (the first 80 rows), and then those parameters should be used to scale both the train and test sets.
3. A vendored third-party TCP server library located at `/app/libtcp-1.0/`. It is meant to be compiled into a static library (`libtcp.a`) that you can link against. However, the package has a deliberate configuration issue that prevents it from building.

Your objectives:
1. **Fix the vendored package:** Identify the build configuration issue in `/app/libtcp-1.0/` and fix it so you can compile `libtcp.a`.
2. **Fix the data leakage:** Modify `/home/user/train.c` so that the `min` and `max` used for normalization are computed strictly over the first 80 rows. Compile and run the fixed `train.c`. It will output a file `/home/user/model.weights` containing the updated parameters: `w`, `b`, `min`, `max`.
3. **Build the inference server:** Write a new C program at `/home/user/server.c` that uses the `libtcp-1.0` library. Your server must:
   - Read the `/home/user/model.weights` file on startup.
   - Listen for raw TCP connections on `127.0.0.1:9000`.
   - The server handler function (from `libtcp`) takes a request string and a response buffer.
   - When a raw TCP request containing a single floating-point number (e.g., `42.5\n`) is received, the server should:
     a) Parse the float `X`.
     b) Scale it using the `min` and `max` loaded from the weights: `X_scaled = (X - min) / (max - min)`.
     c) Compute the prediction: `Y_pred = w * X_scaled + b`.
     d) Write the result formatted exactly as `%.4f\n` into the response buffer.
4. **Deploy:** Compile `server.c` with the `libtcp.a` library and start the server as a background process.

The API of the vendored library (defined in `/app/libtcp-1.0/tcp_server.h`) is:
```c
// tcp_server.h
#ifndef TCP_SERVER_H
#define TCP_SERVER_H

// handler receives a null-terminated request string and must write the null-terminated response into resp_buf.
void start_server(int port, void (*handler)(const char* req, char* resp_buf));

#endif
```

Leave the server running on port 9000 when you are finished. Ensure all your compilation steps use standard tools (e.g., `gcc`, `make`).
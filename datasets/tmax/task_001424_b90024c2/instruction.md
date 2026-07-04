I am a data scientist working on high-throughput DNA melting curve analysis. I have a custom C library that fits non-linear models to spectroscopy data to find the melting temperature (Tm), but my environment setup is broken, and I need a high-performance TCP service to process batch data.

Here is your multi-stage task:

1. **Fix the Vendored Library:**
   You will find a source package located at `/app/libcurvefit-1.0/`. It is supposed to compile into a shared library (`libcurvefit.so`). However, running `make` currently fails due to a configuration/Makefile error related to missing standard library links. 
   - Identify the perturbation in the `Makefile` and fix it.
   - Run `make` to successfully compile `libcurvefit.so`.

2. **Develop an OpenMP-Accelerated TCP Server in C:**
   Write a C program at `/home/user/server.c` that acts as a standalone TCP server. 
   - The server must listen on `127.0.0.1:8080`.
   - When a client connects, it will read a text-based payload. 
   - **Request Format:** 
     The first line will contain a single integer, `N` (the number of melting curves).
     The next `N` lines will each contain exactly 100 space-separated floats. These represent the absorbance values of a DNA sample from 20°C to 119°C (1 float per degree).
   - **Processing:**
     Using OpenMP (`#pragma omp parallel for`), process the `N` curves in parallel.
     For each curve, you must use the vendored library's function:
     `int fit_melting_curve(const float* absorbances, int n_points, float* tm);`
     (Include the header `/app/libcurvefit-1.0/curvefit.h`).
   - **Response Format:**
     For each curve processed, the server must write a line back to the client socket exactly in this format:
     `Curve <index>: Tm = <tm_value>`
     Where `<index>` is the 0-based row index of the curve from the request, and `<tm_value>` is the calculated Tm formatted to 2 decimal places (e.g., `Curve 0: Tm = 68.45`). Keep in mind that while OpenMP processes curves out of order, you must buffer or sort the output so the response lines are sent back to the client in sequential order (Curve 0 to Curve N-1).
   - Once the response is sent, the server can close the client socket and wait for the next connection.

3. **Deploy the Service:**
   Compile your server (make sure to link against OpenMP and your newly compiled `libcurvefit.so`). You may need to set `LD_LIBRARY_PATH`. Run the server in the background so it is actively listening on port 8080. Leave it running.

Your final deliverable is the fixed library and the running TCP server listening on `127.0.0.1:8080`.
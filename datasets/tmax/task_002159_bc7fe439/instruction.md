I need you to deploy a background service that processes spectroscopic data by fitting it to a model using a vendored C++ library. 

However, the provided library has a critical issue. We are using `spectra_fitter-1.0`, located at `/app/spectra_fitter-1.0`. When I try to run its test suite, the internal numerical integrator diverges. It seems there is a logical bug in the step-size adaptation: when the local error exceeds the tolerance, the step size (`dt`) is incorrectly increased instead of being decreased. 

Your tasks are to:
1. Locate the source code for the numerical integrator inside `/app/spectra_fitter-1.0/src/` and fix the step-size adaptation bug (it should halve the step size when the error is too high, but currently it doubles it).
2. Fix any build issues (there might be a missing library link in its `CMakeLists.txt` for standard math functions).
3. Compile and install the library to `/app/installed` (set this as the `CMAKE_INSTALL_PREFIX`).
4. Write a C++ program at `/home/user/service.cpp` that acts as a simple TCP server using standard POSIX sockets. 
5. Compile your server, linking against the installed `spectra_fitter` library.
6. Run the server in the background so it is actively listening.

TCP Server Specifications:
- Listen on `127.0.0.1` port `8181`.
- Accept incoming connections. For each connection, read a single line of text ending with `\n`.
- The line will contain exactly 5 comma-separated floating-point numbers representing a spectral peak (e.g., `0.1,0.5,1.0,0.4,0.1\n`).
- Parse these numbers into a `std::vector<double>` and pass them to the library function: `double SpectraFitter::fit_peak(const std::vector<double>& data);` (available via `#include <spectra_fitter.hpp>`).
- Send back the resulting `double` formatted to 4 decimal places, followed by a newline (e.g., `RESULT: 0.8521\n`), and close the connection.
- The server must continue running and accepting new connections.

Do not use any external frameworks for the server, just standard C++ and POSIX `<sys/socket.h>`. Let me know once the service is compiled, running in the background, and listening on port 8181.
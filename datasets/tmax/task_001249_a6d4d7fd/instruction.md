We are migrating an old mathematical image processing pipeline from a deprecated Python 2 monolithic script to a high-performance Go microservice architecture. The new architecture uses a Go gRPC server that delegates the heavy mathematical computations to a C shared library. 

However, the migration is incomplete and broken:
1. **The Math Specification:** The exact 3x3 convolution kernel used by the legacy Python script was lost during a repository migration, but we recovered a screenshot of the original documentation. It is located at `/app/spec.png`. You need to read this image to determine the exact 9 values of the 3x3 mathematical kernel.
2. **C Library Fixes:** We started porting the convolution logic to C in `/app/clib/filter.c`, but it currently segfaults due to memory safety issues (out-of-bounds access / undefined behavior). The `Makefile` in `/app/clib/` is also broken and fails to link the shared library properly. Fix the C code and the Makefile so that it successfully compiles to `/app/clib/libfilter.so`.
3. **gRPC Service:** Design a protobuf file at `/app/proto/service.proto` defining a `FilterService` with a method `Apply` that takes a `FilterRequest` (containing raw image bytes) and returns a `FilterResponse` (containing processed image bytes).
4. **Go Server & Client:** 
   - Implement the Go gRPC server in `/app/server/main.go` listening on port `50051`. It must use `cgo` to call `libfilter.so`, applying the kernel you extracted from `/app/spec.png` to the incoming image.
   - Implement a Go client in `/app/client/main.go` that reads `/app/input.png`, sends it via gRPC to the server, and saves the returned processed image to `/app/output.png`.

**Requirements:**
- The input and output images are 8-bit grayscale PNGs.
- The C function signature should be `void apply_filter(const unsigned char* in, unsigned char* out, int width, int height, float kernel[9]);`.
- Handle edge pixels by leaving them black (0) or replicating the border, but do not read out of bounds.
- Ensure the server is running and the client has been executed to generate `/app/output.png` before you complete the task.

Generate `/app/output.png` successfully. The accuracy of your convolution and kernel extraction will be measured against a strict metric threshold.
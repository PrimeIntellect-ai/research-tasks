You are tasked with setting up a high-performance polyglot mathematical pipeline that calculates Fast Fourier Transforms (FFTs) using Go and a C library via CGO.

We have a workspace at `/home/user/workspace` containing a Go application `fftapp`. It is intended to benchmark a pure Go FFT implementation against a C implementation. However, the system is currently broken in multiple ways:

1. **Vendored Package & Patching**: The C library we use is `kissfft` version 1.3.1, whose source is pre-vendored at `/app/kissfft-1.3.1`. We have a performance patch located at `/home/user/workspace/patches/kiss_opt.patch` that improves the numerical throughput. However, the patch currently fails to apply due to a deliberate perturbation (mismatched line endings and a slight context conflict). You must fix the patch, apply it, and compile `kissfft` as a shared library (`libkissfft.so`).
2. **Circular Import**: The Go application at `/home/user/workspace/fftapp` currently fails to build due to a circular import between `pkg/processor` and `pkg/utils`. Refactor the Go code to resolve this circular dependency without breaking the API required by `main.go`.
3. **CGO Bindings**: The CGO wrapper in `pkg/cgofft/wrapper.go` is incomplete. You need to implement the CGO bindings to properly allocate C arrays, invoke the `kiss_fft` function from the shared library, and return the result as a Go slice.
4. **Polyglot Build Orchestration**: Write a `Makefile` at `/home/user/workspace/Makefile` that:
   - Builds the `kissfft` shared library and places it in `/home/user/workspace/lib`.
   - Compiles the Go application `fftapp` into a binary at `/home/user/workspace/bin/fftapp`.
   - Ensure the Go binary can find the shared library at runtime (e.g., via `rpath` or `LD_LIBRARY_PATH` wrapper, or by static linking if you prefer, but shared is recommended).

Once the application is built, running `/home/user/workspace/bin/fftapp` will execute a benchmark comparing the pure Go implementation and your CGO implementation on a dataset of 10,000 signals. It outputs a JSON file to `/home/user/workspace/metrics.json`.

**Success Criteria:**
- The Go application compiles successfully.
- `kissfft` is patched and linked correctly.
- The output JSON (`/home/user/workspace/metrics.json`) must demonstrate that the C implementation produces numerically valid results compared to the reference pure Go implementation, and meets a specific performance threshold. 

Your goal is to ensure the complete pipeline builds via `make` and `bin/fftapp` successfully generates `metrics.json` with the optimized CGO implementation outperforming the pure Go version.
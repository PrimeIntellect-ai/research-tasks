You are a developer stepping in to fix a failing build for our high-performance signal processing pipeline. 

The project is located at `/home/user/signal_filter`. It is a Rust application designed to apply a specific 1D convolution to a stream of floating-point numbers provided via standard input, outputting the transformed numbers to standard output. 

Currently, the project has several issues:
1. **Build Failure:** The `Cargo.toml` has a dependency conflict preventing the project from compiling. Fix the dependencies so the project builds successfully in release mode.
2. **Incorrect Parameters:** The previous developer forgot to hardcode the correct kernel and bias. The correct mathematical parameters are embedded in an image left by the research team at `/app/kernel.png`. You must extract the parameters from this image and update the math logic in `src/main.rs`.
3. **Concurrency Bug:** The code attempts to parallelize the convolution using a naive threading model, but there is a race condition causing unpredictable outputs. You must fix the concurrency logic.
4. **Numerical Instability:** The current implementation uses single-precision floats (`f32`) and reorders certain accumulations, causing numerical deviations from our gold standard. You must ensure strictly deterministic `f64` math that perfectly matches our oracle.

We have a pre-compiled reference implementation (oracle) located at `/app/oracle_filter`. 
Your final compiled Rust binary at `/home/user/signal_filter/target/release/signal_filter` must be BIT-EXACT equivalent to the oracle. Both binaries accept a space-separated sequence of numbers via stdin, and output a space-separated sequence of the processed numbers to stdout.

Your task is complete when you have fixed the build, corrected the bugs, updated the parameters based on the image, and successfully compiled the release binary. We will automatically test your binary against the oracle using thousands of randomized inputs.
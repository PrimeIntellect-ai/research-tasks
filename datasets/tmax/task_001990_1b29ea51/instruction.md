You are tasked with fixing a broken hybrid Rust/C project that processes video frames, and subsequently writing property-based tests for its Python equivalent.

The project is located at `/home/user/video_processor`. It contains a Rust application that uses FFI to call a C library (located in `/home/user/video_processor/c_src`) to calculate the average pixel intensity of video frames. Currently, the project fails to compile and build due to a few issues:
1. The C library's `Makefile` is broken and fails to produce the shared object `libintensity.so`.
2. One of the Rust source files (`src/constants.rs`) has a character encoding issue that prevents `rustc` from compiling it.
3. There is a slight mismatch in the FFI declaration in Rust.

Your objectives:
1. **Fix the Makefile:** Repair `/home/user/video_processor/c_src/Makefile` so it correctly compiles `intensity.c` into a shared library `libintensity.so` using position-independent code (`-fPIC`).
2. **Fix the Rust compilation:** Fix the encoding of `src/constants.rs` (it must be valid UTF-8) and correct any FFI signature mismatches in `src/main.rs`. Compile the project using `cargo build --release`. 
3. **Process the Video:** A video file is provided at `/app/test_video.mp4`. 
   - Use `ffmpeg` to extract frames from this video at exactly **5 frames per second**, scaling them to **320x240** resolution, and save them as grayscale raw bytes (`.gray` or `.raw` 8-bit single-channel) in a temporary directory.
   - Run the compiled Rust application: `./target/release/video_processor <path_to_raw_frames_dir> /home/user/output_intensities.json`. The Rust program will output a JSON array of the average intensities for each frame.
4. **Write Property Tests:** A Python equivalent of the intensity function exists in `/home/user/py_src/processor.py`. Write a test suite at `/home/user/py_src/test_processor.py` using `pytest` and `hypothesis`. Create a property-based test that verifies that for any valid `bytes` object representing a 320x240 grayscale image, the Python `calculate_intensity(data: bytes)` function returns a float between 0.0 and 255.0, and does not raise exceptions.

Your final output for the processing pipeline must be the `/home/user/output_intensities.json` file. An automated verifier will compute the Mean Squared Error (MSE) of your frame intensities compared to a golden reference. Your results must achieve an MSE <= 2.0.
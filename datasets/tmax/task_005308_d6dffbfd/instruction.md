You are acting as a release manager preparing our new video processing microservice for deployment. We have a multi-stage pipeline that requires your attention. You must complete the following steps using Bash and standard CLI tools:

1. **Fix the Build Orchestration:**
There is a C++ helper binary located at `/home/user/src/video_processor/` that uses CMake. Currently, `make` fails because it cannot find the shared library `libcustom_filter.so` at link time. The library is located in `/home/user/lib/`.
Write a Bash script at `/home/user/build_pipeline.sh` that:
- Configures the CMake project properly so that it links against `libcustom_filter.so`.
- Compiles the application.
- Copies the resulting `vproc_bin` binary to `/home/user/deploy/bin/`.

2. **Process the Video Fixture:**
As part of the integration test, we ship a standard test video at `/app/test_sequence.mp4`.
Using `ffmpeg` and Bash, extract the frames at 1 frame per second. You must sort and analyze the extracted frames to find the frame that contains the deployment sequence barcode (this barcode appears as a distinct solid white rectangle in the top-left corner of size 50x50 pixels, whereas all other frames have a black top-left corner). 
Write the exact zero-indexed second (e.g., `14`) where this frame occurs into `/home/user/deploy/video_result.txt`.

3. **Reverse Proxy Rule Sanitizer:**
We dynamically load Nginx reverse proxy routing rules, but we have had issues with malicious inputs. 
You must write a Bash script at `/home/user/deploy/validate_routes.sh` that takes a single file path as an argument. The script must parse the Nginx config snippet and exit with code `0` if it is safe, and code `1` if it is malicious.
A file is "malicious" if it contains ANY path traversal sequences (e.g., `../`) in `proxy_pass` directives, or if it exposes port `8080` without a `proxy_set_header Authorization` directive.
Your script will be tested against a corpus of configuration files. 

4. **Integration Testing & Benchmarking:**
Write a final test script at `/home/user/run_integration.sh` that benchmarks `validate_routes.sh` on the entire corpus using `time`, merges all the logs of validation results, and outputs a summary diff against a previous known-good log. 

Ensure your final directory `/home/user/deploy/` contains:
- `bin/vproc_bin`
- `video_result.txt`
- `validate_routes.sh` (must be executable)
- `run_integration.sh`
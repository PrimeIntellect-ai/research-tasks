We have a local video processing pipeline that extracts frames from a security camera feed (`/app/video.mp4`), computes a custom Forward Error Correction (FEC) checksum using a legacy C library, and submits the results to a local validation API.

However, the pipeline is currently broken and extremely slow:
1. **Linking Error**: The C library in `/home/user/fec_lib` fails to compile into a proper shared library, and the Rust tool in `/home/user/video_processor` cannot link against it.
2. **Rate Limiting Bottleneck**: The Rust tool extracts frames using `ffmpeg` and submits checksums to the local validation service (`http://127.0.0.1:8080/submit`) one by one. The service enforces a strict rate limit of 20 requests per second. Since the video has hundreds of frames, the naive sleep/retry logic causes the processing to take way too long.

Your tasks are:
1. Fix the `Makefile` in `/home/user/fec_lib` and the `build.rs` in `/home/user/video_processor` so the Rust crate compiles successfully.
2. Refactor the Rust code (`/home/user/video_processor/src/main.rs`). You must design a custom data structure to collect the processed frame data and utilize the `/batch` endpoint of the local validation service instead. The `/batch` endpoint expects a JSON array of frame objects under the key `"batches"`, and has a much more generous payload capacity (but still limits overall API calls to 5 per second). 
3. Ensure the complete video is processed and successfully accepted by the validation service. 
4. Optimize your Rust application so that the total execution time to process the video and submit all frames is under 3.0 seconds. 

The validation service is running in the background as a systemd service (or you can run `python3 /home/user/validator_service.py &` if it's not active).

When your optimized Rust tool is ready, compile it in release mode. Write a wrapper bash script at `/home/user/run_pipeline.sh` that starts your compiled release binary. An automated test will execute this script, measure its runtime, and verify that all frame checksums were received by the validation service.
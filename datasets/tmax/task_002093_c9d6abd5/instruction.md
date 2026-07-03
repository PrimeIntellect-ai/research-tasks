You are a systems programmer debugging a critical C library linking issue in a Go application. We have a Go project located at `/home/user/vid-parser` that uses `cgo` to interface with a proprietary C library, `libvidproc.so`, located in `/home/user/vid-parser/lib`. 

This C library is designed to process raw video frames and extract embedded metadata. However, the project currently fails to build and run correctly due to a combination of shared library linking issues (the runtime cannot find `libvidproc.so`) and an ABI mismatch in the custom data structure serialization between the C header (`vidproc.h`) and the Go wrapper (`processor.go`).

Additionally, we need to process a test video located at `/app/test_sequence.mp4`. 

Your objectives are:
1. **Fix the Linking and ABI Issues:** Modify `processor.go` and/or the build environment so that the Go application successfully links against `libvidproc.so` both at compile-time and run-time. You must also fix the Go struct definition in `processor.go` so it properly matches the C ABI defined in `vidproc.h` for deserialization. 
2. **Video Extraction:** Use `ffmpeg` (or similar bash-only tools) to extract all frames from `/app/test_sequence.mp4` as raw RGB24 files or PNGs, as required by the application.
3. **Process and Deserialize:** Update the Go application to read these extracted frames, pass them to the C library, and deserialize the returned binary payload. The payload contains a custom binary format encoding a Semantic Version string.
4. **SemVer Sorting:** Implement a custom data structure in Go to correctly parse and sort the extracted semantic versions according to the SemVer 2.0.0 specification (e.g., `1.0.0-alpha` < `1.0.0`).
5. **Output Generation:** The Go application must write the properly sorted semantic versions to `/home/user/sorted_versions.json` as a flat JSON array of strings.

The pipeline must be highly accurate. Due to potential noise in the video, we require an extraction and sorting accuracy of at least 95% compared to the ground truth. Run your finalized Go application to produce the output JSON file.
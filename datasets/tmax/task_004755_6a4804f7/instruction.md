You are a systems programmer debugging a C library linking issue, and you need to build a robust detection system.

In `/home/user/libtrajectory`, there is a small C project with a Makefile that is supposed to compile into a shared library `libtrajectory.so`. However, it currently has a linking error and fails to build. 
1. Fix the Makefile and C source so that `libtrajectory.so` compiles correctly and manages ABI visibility properly.
2. We have a reference video fixture at `/app/camera_feed.mp4`. Use `ffmpeg` to extract its frames and observe the frame metadata (you can dump the metadata using `ffprobe`). This video represents a valid physical trajectory constraint.
3. Write a Go program `/home/user/detector.go` (and accompanying `go.mod`) that uses `cgo` to link against `libtrajectory.so`. The Go program should implement a concurrent gRPC service (or local worker pool using goroutines and channels) to evaluate trajectory data files.
4. The Go program must act as a sanitiser/classifier. It must read a given trajectory text file and determine if it satisfies the physical constraints observed in the video and enforced by the C library. 
5. Create an entry point script `/home/user/run_detector.sh <file_path>` that calls your Go program and exits with code `0` if the file is a valid (clean) trajectory, and a non-zero exit code if it is invalid (evil).

Your solution will be tested against two corpora:
- A "clean" corpus of valid trajectory files.
- An "evil" corpus of invalid trajectory files that violate the constraints (e.g., impossible speeds or teleportation).

Ensure your `run_detector.sh` wrapper is executable and processes exactly one file per invocation, exiting with the correct status code.
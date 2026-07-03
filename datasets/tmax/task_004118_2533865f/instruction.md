You are tasked with building a high-performance artifact manager in Go that curates binary assets extracted from video files. 

Your objective is to write a Go program at `/home/user/curator.go` that performs the following multi-stage pipeline:

1. **Artifact Extraction:** You are provided with a video file at `/app/data/raw_footage.mp4`. Using `ffmpeg` (called via Go's `os/exec`), extract the first 150 frames as JPEG images at a resolution of 640x360.
2. **Concurrent Stream Processing & File Locking:** Spin up multiple goroutines to concurrently process these images. Each goroutine must read an image, compress it into a gzip stream (in-memory), and write the gzipped payload to a unified binary repository folder `/home/user/repo/`. 
   To maintain an audit trail, each goroutine must also append a multi-line log record to a shared log file at `/home/user/repo/audit.log`. Because goroutines run concurrently, you **must** use explicit file locking (e.g., `syscall.Flock`) when writing to the log to prevent corrupted, interleaved log entries. The multi-line log format per frame must be:
   ```
   BEGIN FRAME {frame_number}
   SIZE: {size_in_bytes}
   STATUS: PROCESSED
   END FRAME
   ```
3. **Manifest & Checksum:** After all frames are processed, your Go program must parse the generated `audit.log` (using multi-line log record parsing techniques to reconstruct the exact order and sizes of frames processed). Using this parsed data and the generated files, compute the SHA256 checksum of each `.gz` file and generate a JSON manifest at `/home/user/repo/manifest.json`.
   Format:
   ```json
   {
     "total_frames": 150,
     "artifacts": [
       {"frame": 1, "sha256": "...", "size": ...},
       ...
     ]
   }
   ```

**Performance Constraints:**
Your Go code will be evaluated by an automated testing suite that measures execution speed. You must leverage concurrency effectively. Your compiled binary `/home/user/curator` must complete the entire pipeline (extraction, compression, logging, and manifest generation) in **under 3.0 seconds**.

Write the Go program, compile it, and ensure it runs successfully, producing the required `/home/user/repo` directory, `audit.log`, and `manifest.json`.
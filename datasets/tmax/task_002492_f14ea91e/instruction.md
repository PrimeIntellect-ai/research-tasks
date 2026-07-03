You are an integration developer testing a new API endpoint for a video collaboration platform. The backend processes "video frame patches" to add metadata overlays to specific frames. A previous developer started writing a C extension for the Python backend to validate these patches, but the `setup.py` build is broken and the C code was lost. 

You need to rewrite the core validation logic as a standalone C executable. 

The API receives patch files with the following strict text-based format:
```
FRAME <N>
CRC32 <8-character hex>
@@ <diff header> @@
<patch payload...>
```

**Validation Rules for a "Clean" (Acceptable) Patch:**
1. **Frame Bounds:** The integer `<N>` must be a valid frame index in the source video (0-indexed). It must be `>= 0` and `< TOTAL_FRAMES`. You must dynamically determine the `TOTAL_FRAMES` of the provided video file using `ffprobe` (via `popen` or system calls in your C code).
2. **Checksum Integrity:** The `<8-character hex>` is standard IEEE 802.3 CRC32. It must exactly match the CRC32 computed over the *entire remainder of the file*, starting immediately after the newline following the CRC32 line, through to the end of the file (including all diff headers and payload).
3. **Diff Header Property:** The patch payload MUST begin with the exact string `@@ ` (a standard unified diff header).

If a patch violates *any* of these properties, it is considered malicious or corrupted ("evil") and must be rejected.

**Your Goal:**
1. Write a C program that validates a patch file against a video file.
2. Compile it to exactly `/home/user/validate`.
3. The program must accept exactly two arguments: `/home/user/validate <path_to_video.mp4> <path_to_patch_file>`.
4. It must exit with code `0` if the patch is valid (clean).
5. It must exit with code `1` (or any non-zero code) if the patch is invalid (evil).

You will test your tool against a video provided at `/app/test_sequence.mp4`. Ensure your C code handles file reading and system calls robustly.
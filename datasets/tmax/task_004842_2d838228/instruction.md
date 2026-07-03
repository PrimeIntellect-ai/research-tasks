You are a performance engineer tasked with optimizing a critical data processing pipeline located at `/home/user/event_pipeline`.

The current pure-Python implementation (`slow_pipeline.py`) processes binary event streams but is unacceptably slow. We have a legacy C-compiled processing engine located at `/app/legacy_engine` (which has been stripped of symbols). This legacy engine is the absolute ground truth for correctness, but it is deprecated and cannot be used in production.

Your goal is to create a highly optimized Python script at `/home/user/event_pipeline/fast_pipeline.py` that processes `/home/user/data/events.bin` and outputs the results to `/home/user/event_pipeline/output.bin`. 

During your investigation, you should:
1. Analyze the Git repository at `/home/user/event_pipeline`. A previous engineer attempted a high-performance vector-based implementation using `numpy` and `numba`, but it was reverted because it crashed on corrupted input frames. Additionally, an essential decryption key needed to parse the initial stream header was accidentally committed and then scrubbed from the `HEAD`, but it still exists somewhere in the history.
2. Recover this key and the fast implementation.
3. Fix the bugs in the fast implementation. Specifically, there is an off-by-one boundary condition that causes array out-of-bounds errors when the parser encounters a corrupted event frame (which are intentionally injected into `events.bin` as noise).
4. Trace the intermediate processing states of `/app/legacy_engine` (you can pass single binary frames to it via stdin) to ensure your Python implementation's mathematical logic exactly matches the legacy engine's output.
5. Your final `fast_pipeline.py` must run efficiently. We will measure its execution time and compare its `output.bin` against the expected ground truth.

Your final script must be executable as: `python3 /home/user/event_pipeline/fast_pipeline.py /home/user/data/events.bin /home/user/event_pipeline/output.bin`

Criteria for success:
- The output file must exactly match the legacy engine's logic for all valid frames (corrupted frames must be skipped, outputting nothing for them).
- The execution time must be strictly less than 1.5 seconds.
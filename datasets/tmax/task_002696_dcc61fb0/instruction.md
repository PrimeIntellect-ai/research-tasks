I am debugging a failing build in our custom audio processing package, `audio_biquad`. Our nightly CI is failing because a fuzz test caught a `NaN` output and severe clipping in our custom Direct Form I Biquad filter implementation, causing the test suite to abort.

The repository is located at `/home/user/audio_biquad`.
Inside, you'll find:
- `biquad.py`: The custom filter implementation. It processes audio samples chunk by chunk.
- `fuzz_test.py`: A fuzzing script that generates various extreme audio signals and checks if the filter produces `NaN`, `Inf`, or catastrophic numerical explosions.
- `apply_filter.py`: A CLI tool to apply the filter to an audio file.

Your task is to:
1. Run `pytest fuzz_test.py` or execute it directly to reproduce the floating-point explosion. 
2. Use delta debugging/minimization principles (by modifying the fuzzer or writing your own minimal reproducible script) to isolate the exact signal conditions causing the precision loss.
3. Fix the floating-point precision issue in `biquad.py`. The bug is a classic floating-point stability issue related to the accumulator precision and state variable updates in the Direct Form I implementation when handling low-frequency resonance. You must repair the arithmetic (e.g., by upgrading the internal accumulator precision or rearranging the operations to prevent catastrophic cancellation/overflow) without changing the filter's mathematical transfer function.
4. Once the fuzzer passes without errors, use `apply_filter.py` to process the real audio fixture located at `/app/test_audio.wav`. 
5. Save the successfully filtered output to exactly `/home/user/filtered.wav`.

Our automated evaluation will compute the Mean Squared Error (MSE) between your `/home/user/filtered.wav` and a canonical double-precision reference implementation. To pass, your implementation must produce an MSE of less than `1e-5`. Do not just use a completely different library (like scipy) inside `biquad.py`; you must repair the custom implementation.
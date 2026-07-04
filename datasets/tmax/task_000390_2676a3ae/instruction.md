You are an engineer tasked with fixing and porting a legacy data processing tool, `opti-decode`, to work in a minimal CI container. This Python-based tool extracts encoded binary data from a video file by analyzing the color changes of a specific pixel block over time, using a custom state machine.

Currently, the project is broken in two ways:
1. **Import Ordering/CI Crash:** The test suite used to pass locally on the previous developer's machine due to unpredictable module caching, but in the minimal container, running the tool crashes immediately with a circular import / `AttributeError` related to its plugin registry. 
2. **State Machine Bug:** The core state machine that processes the optical signals drops bytes under certain conditions.

The video file is located at `/app/signal.mp4`. It contains a visual data transmission. 
The top-left pixel (at coordinate x=5, y=5) changes color to encode data:
- **Pure Red (RGB: 255, 0, 0)**: Indicates the "Start of Byte" (Synchronization pulse).
- **Pure Green (RGB: 0, 255, 0)**: Represents a `0` bit.
- **Pure Blue (RGB: 0, 0, 255)**: Represents a `1` bit.

The protocol transmits a byte as follows:
1. One Red frame (Start).
2. Exactly 8 frames of Green or Blue (the 8 bits of the byte, Most Significant Bit first).
3. The next byte immediately follows with another Red frame, or the video ends.
*Note: Due to video compression or frame duplication, a color might persist for multiple consecutive frames. The state machine must process continuous identical colors as a single state (e.g., a sequence of 3 Red frames, 5 Green frames, 2 Blue frames should be parsed as [Red, Green, Blue] -> [Start, 0, 1]).*

Your tasks are:
1. Analyze the source code located in `/home/user/opti-decode/`.
2. Fix the import ordering issues in the `cli.py`, `registry.py`, and `decoder.py` files so the application starts without crashing.
3. Write a small mock test fixture (e.g., `test_mock.py`) that feeds a simulated list of RGB tuples into the parser to help you debug and fix the state machine logic in `decoder.py`. 
4. Modify the state machine to properly reconstruct the ASCII text encoded in the video, applying any diffs/patches to the existing code.
5. Run your fixed tool to process `/app/signal.mp4` and extract the hidden message.
6. Save the final decoded ASCII string to exactly `/home/user/decoded_output.txt`.

Ensure your tool relies on standard libraries and `ffmpeg` (which is pre-installed) to extract frames. You may use temporary directories to store extracted frames or process them in streams. The final verification will evaluate the character-level accuracy of `/home/user/decoded_output.txt` against the ground truth.
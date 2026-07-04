You are a web developer building a real-time UI testing feature that streams video analysis results to a web dashboard. 

The project is currently in a broken state. You have a Go project located in `/home/user/app/` that is supposed to analyze a UI test recording (`/app/ui_test.mp4`), run the frames through a native C shared library for color-state scoring, compute state transitions via a state machine, serialize the results to JSON, and stream them over a WebSocket connection.

Your goals are to fix the build, complete the implementation, and run the server so that it accurately streams the UI states.

1. **Fix the Build (Circular Import & ABI)**
   - The Go code fails to compile due to a circular import between the `streamer` package and the `stateparser` package. Refactor the code to resolve this.
   - The `stateparser` package uses `cgo` to call a provided shared library `/home/user/app/lib/libcolor.so`. However, the Go ABI types do not match the C header (`/home/user/app/lib/color.h`). Fix the `cgo` calls so it correctly interfaces with the shared library.

2. **Frame Extraction and Analysis**
   - The video to analyze is at `/app/ui_test.mp4` (24 fps).
   - You must extract the frames (e.g., using `ffmpeg`, which is preinstalled).
   - For each frame, you must call the `GetColorState(r, g, b)` C function (via your fixed cgo bindings) using the RGB values of the center pixel of the frame.
   
3. **State Machine & Serialization**
   - Implement the missing state machine in `stateparser`. The C library returns an integer representing a color state: `0` (Idle), `1` (Loading), or `2` (Success).
   - Build a parser that groups contiguous frames of the same state into discrete "Events".
   - Serialize these events into a JSON array of objects with the format: `{"state": <int>, "start_frame": <int>, "end_frame": <int>}`.

4. **WebSocket Integration**
   - Update the `streamer` package to serve a WebSocket endpoint at `ws://127.0.0.1:8080/ws`.
   - When a client connects, the server must immediately analyze the video (or use pre-analyzed results) and send the fully serialized JSON array as a single WebSocket text message, then gracefully close the connection.

Run your server in the background so it binds to port 8080. A test script will connect to your WebSocket, retrieve the JSON, and evaluate the accuracy of your state timeline against the true timings in the video. You must achieve a timeline overlap accuracy of at least 0.95.
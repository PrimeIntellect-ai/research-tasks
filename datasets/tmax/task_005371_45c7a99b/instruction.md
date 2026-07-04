You are tasked with building a data querying tool that correlates events extracted from a video feed with an organizational hierarchy provided in a CSV file.

We have a 60-second video at `/app/dashboard.mp4` running at exactly 1 frame per second (60 frames total). Each frame is a solid color representing a different event type:
- Red (#FF0000 or dominant Red channel) = Event R
- Green (#00FF00 or dominant Green channel) = Event G
- Blue (#0000FF or dominant Blue channel) = Event B

Additionally, you are provided with a CSV file at `/home/user/org_chart.csv` with the following columns:
- `dept_id`: Unique string identifier for the department.
- `parent_id`: The `dept_id` of the parent department (empty if it's the root).
- `employees`: Integer representing the number of direct employees in this specific department.

Your objective is to write a Python CLI program at `/home/user/query_tool.py` that takes exactly three positional arguments:
1. `start_sec` (integer, 0-59)
2. `end_sec` (integer, 0-59)
3. `dept_id` (string)

When executed, your script must:
1. Count the number of R, G, and B frames in the video between `start_sec` and `end_sec` (inclusive).
2. Recursively calculate the total number of employees in the department specified by `dept_id` AND all of its descendant departments in the CSV.
3. Multiply the employee total by the count of R, G, and B frames respectively.
4. Print exactly one line to standard output in valid JSON format with the keys `R_score`, `G_score`, and `B_score`, containing the computed values.

Example invocation:
`python3 /home/user/query_tool.py 10 20 D_100`

Expected output format:
`{"R_score": 500, "G_score": 1200, "B_score": 0}`

Constraints:
- You may use `ffmpeg` or `ffprobe` (preinstalled) to extract frames.
- You must use Python 3 to write your script. Standard libraries and `pandas` / `opencv-python` / `Pillow` are available if needed.
- Make sure your script handles recursive hierarchical queries efficiently.
- Your script's output will be strictly verified against an oracle program for multiple random inputs.
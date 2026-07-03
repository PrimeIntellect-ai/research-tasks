# test_final_state.py
import os

def test_tracker_c_exists():
    assert os.path.exists("/home/user/tracker.c"), "The source file /home/user/tracker.c does not exist."

def test_report_html_correctness():
    csv_path = "/home/user/config_stream.csv"
    report_path = "/home/user/report.html"

    assert os.path.exists(csv_path), f"Input file {csv_path} is missing."
    assert os.path.exists(report_path), f"Output file {report_path} was not generated."

    state = {}
    expected_html = ""

    with open(csv_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 4:
                ts, srv, key, val = parts
                state_key = f"{srv}_{key}"
                if state.get(state_key) != val:
                    state[state_key] = val
                    expected_html += (
                        '<div class="change">\n'
                        f'  <span class="time">{ts}</span>\n'
                        f'  <span class="server">{srv}</span>\n'
                        f'  <span class="key">{key}</span>\n'
                        f'  <span class="value">{val}</span>\n'
                        '</div>\n'
                    )

    with open(report_path, "r") as f:
        actual_html = f.read()

    assert actual_html == expected_html, (
        "The generated report.html does not match the expected deduplicated output.\n"
        "Ensure you are extracting state transitions correctly and matching the exact HTML format."
    )
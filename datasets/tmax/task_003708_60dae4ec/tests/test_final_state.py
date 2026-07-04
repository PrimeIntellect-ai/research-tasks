# test_final_state.py
import subprocess
import json
import urllib.request
import urllib.error
import pytest

def get_expected_sizes():
    try:
        out = subprocess.check_output(
            ['ffprobe', '-show_frames', '-select_streams', 'v:0', '-of', 'json', '/app/video.mp4'],
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ffprobe on /app/video.mp4")

    data = json.loads(out)
    frames = sorted(data['frames'], key=lambda x: int(x['coded_picture_number']))

    nodes = {}
    for f in frames:
        idx = int(f['coded_picture_number'])
        nodes[idx] = {
            'type': f['pict_type'],
            'size': int(f['pkt_size']),
            'deps': []
        }

    for i in range(len(frames)):
        if nodes[i]['type'] == 'P':
            # find previous I or P
            for j in range(i-1, -1, -1):
                if nodes[j]['type'] in ('I', 'P'):
                    nodes[i]['deps'].append(j)
                    break
        elif nodes[i]['type'] == 'B':
            # prev I or P
            for j in range(i-1, -1, -1):
                if nodes[j]['type'] in ('I', 'P'):
                    nodes[i]['deps'].append(j)
                    break
            # next I or P
            for j in range(i+1, len(frames)):
                if nodes[j]['type'] in ('I', 'P'):
                    nodes[i]['deps'].append(j)
                    break

    def get_all_deps(idx, visited):
        if idx in visited:
            return
        visited.add(idx)
        for d in nodes[idx]['deps']:
            get_all_deps(d, visited)

    expected_sizes = {}
    for i in nodes.keys():
        visited = set()
        get_all_deps(i, visited)
        total = sum(nodes[v]['size'] for v in visited)
        expected_sizes[i] = total

    return expected_sizes

@pytest.fixture(scope="module")
def expected_sizes():
    return get_expected_sizes()

@pytest.mark.parametrize("test_frame", [0, 2, 5, 10, 15, 19])
def test_dependency_size(expected_sizes, test_frame):
    if test_frame not in expected_sizes:
        pytest.skip(f"Frame {test_frame} not found in video")

    url = f'http://127.0.0.1:8080/dependency_size?frame={test_frame}'
    try:
        req = urllib.request.urlopen(url, timeout=5)
        res = req.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to or read from {url}: {e}")

    try:
        actual_size = int(res)
    except ValueError:
        pytest.fail(f"Expected an integer response, got: '{res}'")

    expected_size = expected_sizes[test_frame]
    assert actual_size == expected_size, f"Frame {test_frame}: expected size {expected_size}, got {actual_size}"
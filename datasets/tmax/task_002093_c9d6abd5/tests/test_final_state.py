# test_final_state.py
import json
import os
import subprocess
import ctypes
import re
from difflib import SequenceMatcher
import pytest

class MetadataPayload(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("frame_id", ctypes.c_uint32),
        ("semver_len", ctypes.c_uint8),
        ("semver_str", ctypes.c_char * 32),
        ("checksum", ctypes.c_uint16),
    ]

def parse_semver(v):
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$", v)
    if not m:
        return (0, 0, 0, [(2,)])
    major, minor, patch, prerelease, build = m.groups()
    major, minor, patch = int(major), int(minor), int(patch)

    if prerelease:
        pre_parts = []
        for p in prerelease.split('.'):
            if p.isdigit():
                pre_parts.append((0, int(p)))
            else:
                pre_parts.append((1, p))
    else:
        pre_parts = [(2,)]

    return (major, minor, patch, pre_parts)

def get_ground_truth():
    video_path = "/app/test_sequence.mp4"
    lib_path = "/home/user/vid-parser/lib/libvidproc.so"

    if not os.path.exists(video_path) or not os.path.exists(lib_path):
        pytest.skip("Required files for ground truth generation are missing.")

    # Get video dimensions
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", video_path
    ]
    try:
        output = subprocess.check_output(cmd, text=True).strip()
        width, height = map(int, output.split('x'))
    except Exception as e:
        pytest.fail(f"Failed to get video dimensions: {e}")

    # Extract raw frames
    cmd = [
        "ffmpeg", "-i", video_path, "-f", "image2pipe",
        "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "-"
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        raw_video, _ = proc.communicate()
    except Exception as e:
        pytest.fail(f"Failed to extract video frames: {e}")

    frame_size = width * height * 3
    num_frames = len(raw_video) // frame_size

    lib = ctypes.CDLL(lib_path)
    lib.process_frame.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
    lib.process_frame.restype = ctypes.POINTER(MetadataPayload)
    lib.free_payload.argtypes = [ctypes.POINTER(MetadataPayload)]
    lib.free_payload.restype = None

    versions = []
    for i in range(num_frames):
        frame_data = raw_video[i*frame_size : (i+1)*frame_size]
        payload_ptr = lib.process_frame(frame_data, width, height)
        if payload_ptr:
            payload = payload_ptr.contents
            semver = payload.semver_str[:payload.semver_len].decode('utf-8', errors='ignore')
            versions.append(semver)
            lib.free_payload(payload_ptr)

    versions.sort(key=parse_semver)
    return versions

def test_sorted_versions_accuracy():
    output_file = "/home/user/sorted_versions.json"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    try:
        with open(output_file, "r") as f:
            agent_output = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {output_file}: {e}")

    assert isinstance(agent_output, list), "Output JSON must be a list of strings."

    ground_truth = get_ground_truth()

    matcher = SequenceMatcher(None, ground_truth, agent_output)
    accuracy = matcher.ratio()

    assert accuracy >= 0.95, f"SequenceMatcher accuracy {accuracy:.4f} is below threshold 0.95"
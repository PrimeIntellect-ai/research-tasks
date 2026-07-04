# test_final_state.py
import os
import struct
import io
import pytest
from PIL import Image

ARCHIVE_PATH = '/home/user/doc_archive.pak'

def test_archive_exists_and_size():
    """Verify the archive exists and meets the size constraint."""
    assert os.path.exists(ARCHIVE_PATH), f"Archive not found at {ARCHIVE_PATH}"
    size = os.path.getsize(ARCHIVE_PATH)
    assert size < 150000, f"Archive too large: {size} bytes (must be < 150000)"

def test_archive_structure_and_contents():
    """Verify the custom binary format and the contents of the files inside."""
    assert os.path.exists(ARCHIVE_PATH), f"Archive not found at {ARCHIVE_PATH}"

    with open(ARCHIVE_PATH, 'rb') as f:
        magic = f.read(8)
        assert magic == b'DOCARCH1', f"Invalid magic header: {magic}"

        file_count_data = f.read(2)
        assert len(file_count_data) == 2, "Unexpected EOF reading file count"
        file_count = struct.unpack('<H', file_count_data)[0]
        assert file_count == 8, f"Expected 8 files (1 md + 7 jpgs), found {file_count}"

        files = {}
        for _ in range(file_count):
            nl_data = f.read(1)
            assert len(nl_data) == 1, "Unexpected EOF reading filename length"
            name_len = struct.unpack('B', nl_data)[0]

            name_data = f.read(name_len)
            assert len(name_data) == name_len, "Unexpected EOF reading filename"
            name = name_data.decode('ascii')

            size_data = f.read(4)
            assert len(size_data) == 4, "Unexpected EOF reading file size"
            file_size = struct.unpack('<I', size_data)[0]

            data = f.read(file_size)
            assert len(data) == file_size, "Unexpected EOF reading file data"
            files[name] = data

    # Verify final_doc.md
    assert 'final_doc.md' in files, "final_doc.md missing from archive"
    md_text = files['final_doc.md'].decode('utf-8')

    expected_lines = [
        "![00:02](frame_00_02.jpg) The system boots up and shows the initialization screen.",
        "![00:06](frame_00_06.jpg) The user navigates to the main configuration menu.",
        "![00:12](frame_00_12.jpg) Network settings are opened.",
        "![00:15](frame_00_15.jpg) IP address is configured.",
        "![00:18](frame_00_18.jpg) Changes are saved and applied.",
        "![00:22](frame_00_22.jpg) A confirmation dialog appears.",
        "![00:25](frame_00_25.jpg) The system reboots."
    ]

    for expected in expected_lines:
        assert expected in md_text, f"Expected markdown line missing or incorrect: {expected}"

    # Verify images
    expected_images = [
        'frame_00_02.jpg', 'frame_00_06.jpg', 'frame_00_12.jpg',
        'frame_00_15.jpg', 'frame_00_18.jpg', 'frame_00_22.jpg', 'frame_00_25.jpg'
    ]

    for img_name in expected_images:
        assert img_name in files, f"{img_name} missing from archive"

        # Load image from bytes
        img_data = files[img_name]
        try:
            img = Image.open(io.BytesIO(img_data))
            img.load()
        except Exception as e:
            pytest.fail(f"Failed to open {img_name} as a valid image: {e}")

        assert img.format in ['JPEG', 'MPO'], f"{img_name} is not a JPEG (got {img.format})"
        assert img.size == (320, 240), f"{img_name} has wrong dimensions: {img.size} (expected 320x240)"

        # Check if grayscale (could be 'L' mode or RGB but with all channels equal)
        # If it's saved as JPEG, it might be converted to RGB, but we can verify color content
        if img.mode != 'L':
            # Convert to RGB if not already
            img_rgb = img.convert('RGB')
            # Check a few pixels to see if R==G==B
            w, h = img_rgb.size
            pixels = img_rgb.load()
            for x in range(0, w, 10):
                for y in range(0, h, 10):
                    r, g, b = pixels[x, y]
                    # Allow slight variations due to JPEG compression
                    assert abs(r - g) <= 5 and abs(g - b) <= 5, f"{img_name} does not appear to be grayscale"
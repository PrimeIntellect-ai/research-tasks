# test_final_state.py

import os
import pytest

def test_archive_db_exists_and_compressed():
    """Test that archive.db exists and achieves the required compression ratio."""
    archive_path = '/home/user/archive.db'
    assets_dir = '/home/user/assets'

    assert os.path.exists(archive_path), f"Output file {archive_path} does not exist."
    assert os.path.isfile(archive_path), f"Output path {archive_path} is not a file."

    archive_size = os.path.getsize(archive_path)

    # Calculate original size from assets directory if it exists, otherwise fallback to the known original size
    if os.path.exists(assets_dir) and os.path.isdir(assets_dir):
        original_size = sum(
            os.path.getsize(os.path.join(assets_dir, f))
            for f in os.listdir(assets_dir)
            if os.path.isfile(os.path.join(assets_dir, f))
        )
    else:
        # Fallback to the known original size if the agent deleted the assets directory
        original_size = 104857600

    assert original_size > 0, "Original size is 0, cannot compute compression ratio."
    assert archive_size > 0, f"Archive file {archive_path} is empty."

    ratio = original_size / archive_size
    threshold = 2.85

    assert ratio >= threshold, (
        f"Compression ratio too low. "
        f"Original size: {original_size} bytes, Archive size: {archive_size} bytes. "
        f"Ratio achieved: {ratio:.2f}x. Required ratio: >= {threshold}x."
    )
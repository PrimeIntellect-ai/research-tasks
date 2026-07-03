# test_final_state.py
import os

def test_final_pipeline_patch_exists():
    """Check if the final_pipeline.patch file exists."""
    patch_path = "/home/user/final_pipeline.patch"
    assert os.path.isfile(patch_path), f"The file {patch_path} does not exist."

def test_final_pipeline_patch_content():
    """Check if the final_pipeline.patch file contains the correct, sorted diffs without the CMakeLists.txt diff."""
    patch_path = "/home/user/final_pipeline.patch"
    with open(patch_path, "r") as f:
        content = f.read().strip()

    expected_content = """--- a/assets/config.json
+++ b/assets/config.json
@@ -5,2 +5,3 @@
     "version": "1.0",
-    "debug": false
+    "debug": false,
+    "auto_update": true
 }
--- a/src/audio.c
+++ b/src/audio.c
@@ -2,3 +2,3 @@
 void play_sound() {
-    return 0;
+    return 1;
 }
--- a/src/video.c
+++ b/src/video.c
@@ -10,3 +10,4 @@
 void init_video() {
-    printf("Init video old");
+    printf("Init video new");
+    setup_buffers();
 }"""

    # Normalize line endings to prevent failures due to CRLF/LF differences
    content_normalized = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    expected_normalized = "\n".join(line.strip() for line in expected_content.splitlines() if line.strip())

    assert "native_camera" not in content, "The CMakeLists.txt diff containing 'native_camera' was not removed."
    assert content_normalized == expected_normalized, "The final_pipeline.patch content does not match the expected sorted diffs."
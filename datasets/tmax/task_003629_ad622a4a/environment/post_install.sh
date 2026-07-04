apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest websockets

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/ws_server.py
import asyncio
import websockets
import sys

payload = """--- a/src/video.c
+++ b/src/video.c
@@ -10,3 +10,4 @@
 void init_video() {
-    printf("Init video old");
+    printf("Init video new");
+    setup_buffers();
 }
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -45,3 +45,2 @@
 add_executable(myapp main.cpp)
-target_link_libraries(myapp native_camera)
 target_link_libraries(myapp audio_engine)
--- a/src/audio.c
+++ b/src/audio.c
@@ -2,3 +2,3 @@
 void play_sound() {
-    return 0;
+    return 1;
 }
--- a/assets/config.json
+++ b/assets/config.json
@@ -5,2 +5,3 @@
     "version": "1.0",
-    "debug": false
+    "debug": false,
+    "auto_update": true
 }
"""

async def handler(websocket, path):
    await websocket.send(payload)
    await websocket.close()

async def main():
    async with websockets.serve(handler, "127.0.0.1", 9753):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
EOF

    chmod -R 777 /home/user
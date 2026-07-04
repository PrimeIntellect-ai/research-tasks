apt-get update && apt-get install -y python3 python3-pip gcc make patch
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/libprocess.c
#include <string.h>

void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}
EOF

    cat << 'EOF' > /home/user/Makefile
libprocess.so: libprocess.c
	gcc -shared -fPIC -o libprocess.so libprocess.c
EOF

    cat << 'EOF' > /home/user/process.py
import ctypes
import sys

lib = ctypes.CDLL('./libprocess.so')

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.read().strip()

    # In python 2, data is bytes
    buf = ctypes.create_string_buffer(data)
    lib.reverse_string(buf)

    with open(output_file, 'w') as f:
        f.write(buf.value)

if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2])
EOF

    cat << 'EOF' > /home/user/py3_migration.patch
--- process.py
+++ process.py
@@ -4,12 +4,12 @@
 lib = ctypes.CDLL('./libprocess.so')

 def process_file(input_file, output_file):
-    with open(input_file, 'r') as f:
+    with open(input_file, 'r', encoding='latin-1') as f:
         data = f.read().strip()

-    # In python 2, data is bytes
-    buf = ctypes.create_string_buffer(data)
+    # Python 3 migration
+    buf = ctypes.create_string_buffer(data.encode('utf-8'))
     lib.reverse_string(buf)

-    with open(output_file, 'w') as f:
-        f.write(buf.value)
+    with open(output_file, 'w', encoding='latin-1') as f:
+        f.write(buf.value.decode('utf-8'))
EOF

    python3 -c "open('/home/user/input.txt', 'wb').write(b'caf\xe9')"
    python3 -c "open('/home/user/expected.txt', 'wb').write(b'\xe9fac')"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
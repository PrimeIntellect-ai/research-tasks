apt-get update && apt-get install -y python3 python3-pip binutils
pip3 install pytest pyinstaller

# Create the /app directory
mkdir -p /app

# Create a dummy python script to be compiled into an ELF binary
cat << 'EOF' > /tmp/doc_packager.py
#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: doc_packager <input_dir> <output_file>")
        sys.exit(1)
    print("Packing...")

if __name__ == "__main__":
    main()
EOF

# Compile the script into a standalone ELF binary
pyinstaller --onefile /tmp/doc_packager.py -n doc_packager --distpath /app

# Strip the binary as per instructions
strip /app/doc_packager

# Ensure it's executable
chmod +x /app/doc_packager

# Clean up build files
rm -rf /tmp/doc_packager.py build doc_packager.spec

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
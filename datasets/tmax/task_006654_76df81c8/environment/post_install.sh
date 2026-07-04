apt-get update && apt-get install -y python3 python3-pip binutils coreutils gawk grep
pip3 install pytest

useradd -m -s /bin/bash user || true

# Generate access.log
cat << 'EOF' > /home/user/generate_logs.sh
#!/bin/bash
echo "192.168.1.15 - - [10/Oct/2023:13:55:36 +0000] \"GET / HTTP/1.1\" 200" > /home/user/access.log
echo "10.0.0.5 - - [10/Oct/2023:13:55:40 +0000] \"GET /api HTTP/1.1\" 200" >> /home/user/access.log
# Anomalous IP: 172.16.45.99 at 13:56
for i in {1..1337}; do
    echo "172.16.45.99 - - [10/Oct/2023:13:56:15 +0000] \"POST /login HTTP/1.1\" 401" >> /home/user/access.log
done
# Add some more noise
for i in {1..500}; do
    echo "192.168.1.15 - - [10/Oct/2023:13:57:01 +0000] \"GET / HTTP/1.1\" 200" >> /home/user/access.log
done
EOF
chmod +x /home/user/generate_logs.sh
/home/user/generate_logs.sh
rm /home/user/generate_logs.sh

# Generate build.log
echo "Starting build..." > /home/user/build.log
for i in {1..5000}; do echo "Compiling module_$i.c... OK" >> /home/user/build.log; done
echo "Linking executable..." >> /home/user/build.log
echo "/usr/bin/ld: /tmp/ccABCDEF.o: in function \`main':" >> /home/user/build.log
echo "legacy_parser.c:(.text+0x42): undefined reference to \`lib_crypto_verify_v2'" >> /home/user/build.log
echo "collect2: error: ld returned 1 exit status" >> /home/user/build.log
for i in {1..100}; do echo "make: *** [Makefile:12: all] Error 1" >> /home/user/build.log; done

# Generate fake binary
head -c 10000 /dev/urandom > /home/user/legacy_parser
echo -n "DEBUG_PWD=SuperSecretDev0ps_99!" >> /home/user/legacy_parser
head -c 5000 /dev/urandom >> /home/user/legacy_parser
chmod +x /home/user/legacy_parser

chmod -R 777 /home/user
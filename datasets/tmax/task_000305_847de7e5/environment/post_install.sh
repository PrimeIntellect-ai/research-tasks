apt-get update && apt-get install -y python3 python3-pip wget build-essential
    pip3 install pytest packaging

    useradd -m -s /bin/bash user || true

    # Generate dataset
    cat << 'EOF' > /tmp/gen_data.py
import random
import os

random.seed(42)
versions = []
for _ in range(100000):
    major = random.randint(0, 10)
    minor = random.randint(0, 50)
    patch = random.randint(0, 100)
    has_prerelease = random.choice([True, False])
    if has_prerelease:
        prerelease = f"alpha.beta.{random.randint(10000000000, 99999999999)}" # Long string to trigger overflow
        versions.append(f"{major}.{minor}.{patch}-{prerelease}")
    else:
        versions.append(f"{major}.{minor}.{patch}")

with open("/home/user/versions.txt", "w") as f:
    f.write("\n".join(versions))
EOF
    python3 /tmp/gen_data.py

    # Vendor semver.c
    mkdir -p /app/semver.c-1.0.0
    cd /app/semver.c-1.0.0
    wget -q https://raw.githubusercontent.com/h2non/semver.c/v1.0.0/semver.c
    wget -q https://raw.githubusercontent.com/h2non/semver.c/v1.0.0/semver.h

    # Introduce the vulnerability
    cat << 'EOF' > /tmp/perturb.py
with open("semver.c", "r") as f:
    content = f.read()

# Try different spacing variations of the function signature
target1 = "int semver_parse(const char *str, semver_t *ver) {"
target2 = "int semver_parse (const char *str, semver_t *ver) {"
target3 = "int\nsemver_parse(const char *str, semver_t *ver) {"
target4 = "int\nsemver_parse (const char *str, semver_t *ver) {"

vuln = "{\n  char buf[12];\n  strcpy(buf, str);\n"

if target1 in content:
    content = content.replace(target1, target1[:-1] + vuln)
elif target2 in content:
    content = content.replace(target2, target2[:-1] + vuln)
elif target3 in content:
    content = content.replace(target3, target3[:-1] + vuln)
elif target4 in content:
    content = content.replace(target4, target4[:-1] + vuln)
else:
    # Fallback if signature format is unexpected
    content = content.replace("int semver_parse", "int semver_parse_orig")
    wrapper = """
int semver_parse(const char *str, semver_t *ver) {
  char buf[12];
  strcpy(buf, str);
  return semver_parse_orig(str, ver);
}
"""
    content += wrapper

with open("semver.c", "w") as f:
    f.write(content)
EOF
    python3 /tmp/perturb.py

    chmod -R 777 /home/user
    chmod -R 777 /app
import os

def is_safe_path(base_dir, requested_path):
    # Resolve the absolute path of the base directory
    absolute_base = os.path.abspath(base_dir)

    # Construct the full requested path
    full_requested_path = os.path.join(absolute_base, requested_path)

    # Resolve the absolute, canonical path of the requested file
    # This resolves any ../ or symlinks
    canonical_requested_path = os.path.abspath(full_requested_path)

    # Ensure the resolved path starts with the base directory
    # os.path.commonpath ensures we don't fall victim to partial directory name matches
    # (e.g., /var/www/uploads vs /var/www/uploads_backup)
    return os.path.commonpath([absolute_base, canonical_requested_path]) == absolute_base

# Example usage
base_directory = "/var/www/uploads"

# Safe request
print(is_safe_path(base_directory, "image.png")) # True

# Malicious request
print(is_safe_path(base_directory, "../../../etc/passwd")) # False
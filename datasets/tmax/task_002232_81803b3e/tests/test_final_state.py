# test_final_state.py

import os
import json
import pytest

def get_migration_mapping(log_path):
    mapping = {}
    if not os.path.exists(log_path):
        return mapping

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    original = None
    for line in lines:
        if line.startswith("Original: "):
            original = line.split("Original: ", 1)[1].strip()
        elif line.startswith("New: "):
            new_file = line.split("New: ", 1)[1].strip()
            if original:
                mapping[original] = new_file
                original = None
    return mapping

def test_symlinks_created_correctly():
    sitemap_path = '/home/user/sitemap.json'
    log_path = '/home/user/migration.log'
    docs_portal = '/home/user/docs_portal'
    raw_docs = '/home/user/raw_docs'

    assert os.path.isfile(sitemap_path), f"Expected sitemap file at {sitemap_path} is missing."
    assert os.path.isfile(log_path), f"Expected migration log file at {log_path} is missing."

    with open(sitemap_path, 'r') as f:
        try:
            sitemap = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {sitemap_path} is not valid JSON.")

    mapping = get_migration_mapping(log_path)
    assert mapping, "Failed to parse any mappings from migration.log."

    for category, articles in sitemap.items():
        category_dir = os.path.join(docs_portal, category)
        assert os.path.isdir(category_dir), f"Expected category directory is missing: {category_dir}"

        for article_title, old_filename in articles.items():
            symlink_path = os.path.join(category_dir, f"{article_title}.md")

            assert old_filename in mapping, f"Could not find a mapping for original file '{old_filename}' in migration.log."
            new_filename = mapping[old_filename]
            expected_target = os.path.join(raw_docs, new_filename)

            assert os.path.islink(symlink_path), (
                f"Expected a symbolic link at {symlink_path}, but it is missing or not a symlink."
            )

            actual_target = os.readlink(symlink_path)
            assert actual_target == expected_target, (
                f"Symlink at {symlink_path} points to '{actual_target}', "
                f"but it should point to the absolute path '{expected_target}'."
            )
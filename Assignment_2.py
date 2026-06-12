"""
build_version_updater.py
Updates build version number in SConstruct and VERSION files.
"""

import os
import re
import sys
import logging


# logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# read environment variables

def get_env():
    build_num   = os.environ.get("BuildNum")
    source_path = os.environ.get("SourcePath")

    if not build_num:
        logging.error("BuildNum environment variable not set!")
        sys.exit(1)

    if not source_path:
        logging.error("SourcePath environment variable not set!")
        sys.exit(1)

    return build_num, source_path

# update version in any file

def update_file(file_path, pattern, replacement):
    # check file exists
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

    logging.info(f"Updating: {file_path}")

    # read file
    with open(file_path, 'r') as f:
        content = f.read()

    # check pattern exists
    if not re.search(pattern, content):
        logging.warning(f"Pattern not found in {file_path} — skipping!")
        return

    # replace pattern
    new_content = re.sub(pattern, replacement, content)

    # write back to file
    with open(file_path, 'w') as f:
        f.write(new_content)

    logging.info(f"✅ Done: {file_path}")

# main

def main():
    # step 1 — get env variables
    build_num, source_path = get_env()

    # step 2 — build src path
    src_path = os.path.join(
        source_path, "develop", "global", "src"
    )

    # step 3 — update SConstruct
    update_file(
        file_path   = os.path.join(src_path, "SConstruct"),
        pattern     = r"point=\d+",
        replacement = f"point={build_num}"
    )

    # step 4 — update VERSION
    update_file(
        file_path   = os.path.join(src_path, "VERSION"),
        pattern     = r"ADLMSDK_VERSION_POINT=\d+",
        replacement = f"ADLMSDK_VERSION_POINT={build_num}"
    )

    logging.info("✅ All files updated successfully!")

# entry point

if __name__ == "__main__":
    main()
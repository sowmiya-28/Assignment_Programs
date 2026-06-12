import os
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_env_variables():
    
    build_number = os.environ.get("BuildNum")
    source_path = os.environ.get("SourcePath")
    
    if not build_number:
        logging.error("BuildNum environment variable is missing")
        sys.exit(1)
        
    if not source_path:
        logging.error("SourcePath environment variable is missing")
        sys.exit(1)
    
    print("Environment variables loaded successfully")
    return build_number, source_path


def update_file(filepath, pattern, replacement):
    
    # check if the file exists before opening
    if not os.path.exists(filepath):
        logging.error("Cannot find the file: " + filepath)
        sys.exit(1)
    
    print("Opening file: " + filepath)
    
    # open and read the file content
    f = open(filepath, 'r')
    content = f.read()
    f.close()
    
    # check if pattern exists in file
    if not re.search(pattern, content):
        logging.warning("Could not find the pattern in file, skipping: " + filepath)
        return
    
    # replace old version number with new build number
    updated_content = re.sub(pattern, replacement, content)
    
    # write updated content back to same file
    f = open(filepath, 'w')
    f.write(updated_content)
    f.close()
    
    print("File updated: " + filepath)
    logging.info("Version number updated in: " + filepath)


def main():
    
    print("Starting version update...")
    
    # get build number and source path from environment
    build_number, source_path = get_env_variables()
    
    # build the full path to src directory
    source_dir = os.path.join(source_path, "develop", "global", "src")
    
    # set file paths
    sconstruct_file = os.path.join(source_dir, "SConstruct")
    version_file = os.path.join(source_dir, "VERSION")
    
    # update version number in SConstruct file
    update_file(sconstruct_file, "point=[\d]+", "point=" + build_number)
    
    # update version number in VERSION file
    update_file(version_file, "ADLMSDK_VERSION_POINT=[\d]+", "ADLMSDK_VERSION_POINT=" + build_number)
    
    print("Version update completed successfully!")
    logging.info("All files updated with build number: " + build_number)


if __name__ == "__main__":
    main()

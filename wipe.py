import os
import sys
import time
import string
import random
from random import getrandbits

def write_random_data(file, size_in_mb):
    if size_in_mb >= 1:
        chunk_size = 1024 * 1024  # 1MB chunk
        num_chunks = size_in_mb
    else:
        chunk_size = 1024  # 1 KB chunk
        num_chunks = int(size_in_mb * 1024)  # Convert MB to KB

    for _ in range(num_chunks):
        file.write(getrandbits(8 * chunk_size).to_bytes(chunk_size, 'little'))

def fill_drive_with_random_data(drive, file_sizes):
    total_written = 0
    file_count = 0
    file_names = []
    random_string = ""

    for size in file_sizes:
        while True:
            try:
                random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                file_name = f"{drive}:/random_data_{file_count}_{random_string}.bin"
                with open(file_name, "wb") as file:
                    write_random_data(file, size)
                total_written += size
                file_count += 1
                file_names.append(file_name)
                print(f"Written {file_count} files, {total_written} MB so far.")
            except IOError:
                break  # No more space left for this file size

    return file_names

def delete_all_files(file_names):
    for file_name in file_names:
        try:
            os.remove(file_name)
            #print(f"Deleted {file_name}")
        except OSError as e:
            print(f"Error deleting {file_name}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python wipe.py <drive_letter>")
        print("Example: python wipe.py E")
        sys.exit(1)

    drive = sys.argv[1].upper()
    if drive not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print("Invalid drive letter.")
        sys.exit(1)

    confirm = input(f"WARNING: This will delete ALL data on the {drive}: drive. You hereby accept full responsibility for any accidental loss or later recovery of data with this script.\r\n\r\nThis might take a long time depending on what kind of USB drive you have. Connecting the USB device directly to your computer (not a USB hub or adapter) can give faster speeds. If you have a SSD drive then you will have to run this several times. \r\n\r\nAre you sure you want to continue and wipe drive {drive}:? (yes/no): ")
    if confirm.lower() != "yes":
        print("Operation canceled.")
        sys.exit(1)
    print("Deleting all files on drive...")
    delete_all_files([os.path.join(root, file) for root, _, files in os.walk(f"{drive}:/") for file in files])

    file_sizes = [500, 100, 10, 1, 0.001]  # In megabytes
    print("Filling drive with random data files to overwrite all free space...")
    created_files = fill_drive_with_random_data(drive, file_sizes)
    print("Removing random files...")
    delete_all_files(created_files)
    print("Cleaning up...")
    delete_all_files([os.path.join(root, file) for root, _, files in os.walk(f"{drive}:/") for file in files])
    print("Script completed. The drive has been wiped.")

if __name__ == "__main__":
    main()

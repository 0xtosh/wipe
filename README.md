# wipe
 Poor man's wipe utility for non-administrator users by filling up the drive with random data

# Description
This Python script is a slow poor man's wipe script to fill up a specified drive with progressively smaller files until the drive is completely filled. It is useful for wiping data from a drive by filling up all the free space with a single pass of random data. The script adapts the file size dynamically based on the available space on the drive until full. If you have a SSD drive connected you will have to run it several times.

# How does it work
Run the script with the target drive letter as an argument, e.g., python wipe.py E:

It then:
- Deletes all existing files on the specified drive
- Starts filling it with progressively smaller files
- Deletes all the random data 

Use this script responsibly, as it will delete all data on the specified drive.

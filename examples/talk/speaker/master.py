#!/usr/bin/env python3
"""
Script to find all files matching pattern "out-(number).wav" and create a files.txt
with entries in the format "file '(filename)'"
"""

import os
import re
import glob
import subprocess


def main():
    # Pattern to match files like "out-1.wav", "out-123.wav", etc.
    pattern = "out-*.wav"

    # Find all matching files in current directory
    wav_files = glob.glob(pattern)

    # Filter to ensure they match the exact pattern "out-(number).wav"
    # This regex ensures we only get files with numbers after "out-"
    number_pattern = re.compile(r"^out-.*\d+\.wav$")
    filtered_files = [f for f in wav_files if number_pattern.match(f)]

    # Sort files numerically by the number in the filename
    def extract_number(filename):
        match = re.search(r"out-.*(\d+)\.wav", filename)
        return int(match.group(1)) if match else 0

    filtered_files.sort(key=extract_number)

    # Create the output file
    with open("files.txt", "w") as output_file:
        for wav_file in filtered_files:
            output_file.write(f"file '{wav_file}'\n")

    print(f"Found {len(filtered_files)} matching files:")
    for wav_file in filtered_files:
        print(f"  {wav_file}")
    print(f"Created files.txt with {len(filtered_files)} entries")

    subprocess.run(["ffmpeg -f concat -i files.txt -c copy master.wav"], shell=True)

    subprocess.run("ffplay master.wav", shell=True)


if __name__ == "__main__":
    main()

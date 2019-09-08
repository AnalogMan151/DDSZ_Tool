#!/usr/bin/env python3
# Author: AnalogMan
# Modified Date: 2019-09-07
# Purpose: Compress/Decompress DDSZ files for Switch 
# Requirements: LZ4 (pip install lz4)

import sys, os, lz4.block, argparse

def main():
    print('\n======== DDSZ Archive Tool ========\n\n')

    if sys.version_info <= (3,1,0):
        print('Python version 3.1.x+ needed to run this script.\n\n')
        return 1    
    
    # Arg parser for program options
    parser = argparse.ArgumentParser(description='Process DDSZ files with LZ4')
    parser.add_argument('filename', help='Path to file')

    # Check passed arguments
    args = parser.parse_args()

    # Check if required files exist
    if os.path.isfile(args.filename) == False:
        print('File cannot be found.\n')
        return 1
    
    filename = args.filename

    # If DDSZ, decompress RAW block
    if (filename[-4:].lower()) == 'ddsz':
        try:
            with open(filename, 'rb') as f:
                compressed = f.read()
            with open(filename[:-4] + 'dds', 'wb') as f:
                f.write(lz4.block.decompress(compressed[4:]))
            print('DDS file decompressed successfully.\n\n')
        except:
            print('Could not decompress file.\n\n')

    # If DDS, compress to DDSZ and include filesize.
    elif (filename[-3:].lower()) == 'dds':
        try:
            with open(filename, 'rb') as f:
                decompressed = f.read()
            with open(filename[:-3] + 'ddsz', 'wb') as f:
                compressed = lz4.block.compress(decompressed)
                f.write((len(compressed)+4).to_bytes(4, byteorder='little', signed=True))
                f.write(compressed)
            print('DDS file compressed successfully.\n\n')
        except:
            print('Could not compress file.\n\n')
    else:
        print('Unsupported file.\n')
        return 1

if __name__ == "__main__":
    main()

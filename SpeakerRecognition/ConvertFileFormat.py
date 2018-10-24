import os
import sys

def convert(filename):
    new_filename = filename.split('.')[0] + '.wav'
    os.system("ffmpeg -y -i {0} -acodec pcm_s16le -ac 1 -ar 16000 {1}".format(filename, new_filename))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python ConvertFileFormat.py <filename>')
        sys.exit('Error: Incorrect Usage.')

    convert(sys.argv[1])
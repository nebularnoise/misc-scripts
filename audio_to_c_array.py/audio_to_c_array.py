import soundfile as sf
import numpy
import math
import os
import argparse

formats = ['wav', 'aif', 'aiff', 'ogg', 'flac', 'mp3', 'aac', 'raw']


def array_to_header(data, h_filename, array_name, data_format):
    h_file = open(h_filename, "w")
    h_file.write(data_format + " " + array_name + " [" + str(len(data)) + "] = {\n\t\t")

    if data_format == "float":
        h_file.write(',\n\t\t'.join("%10.24f" % x for x in data))
    if data_format == "int":
        h_file.write(',\n\t\t'.join("%i" % math.floor(x * 32618) for x in data))
    if data_format == "altu8":
        h_file.write(',\n\t\t'.join("%i" % math.floor(128 + x * 128) for x in data))
    h_file.write("\n};\n")
    h_file.close()


def convert_to_mono(stereo_data, channels):
    mono_data = numpy.zeros(len(stereo_data))
    for i in range(0, len(stereo_data) - 1):
        mono_data[i] = sum(stereo_data[i]) / channels
    return mono_data


def parse_paths(paths):
    wavefiles = []
    for path in args.paths:
        if os.path.isfile(path):
            wavefiles.append(path)
        if os.path.isdir(path):
            for path, subdirs, files in os.walk(path):
                for name in files:
                    if os.path.splitext(name)[1] in formats:
                        wavefiles.append(os.path.join(path, name))
    return wavefiles


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="WAV to C array")
    parser.add_argument("paths", metavar="path(s)", type=str, nargs='+',
                        help="Path to WAV file, or directory containing wav files")

    #parser.add_argument("-o", "--output", type=str, help="Path to write output")
    parser.add_argument("-s", "--stereo", action="store_true", help = "Output interlaced stereo array")
    parser.add_argument("-f", "--format", type=str, help="C data format (float, int or altu8)", default="float")
    args = parser.parse_args()

    wav_files = parse_paths(args.paths)
    for wav in wav_files:
        h_filename = os.path.splitext(wav)[0] + ".h"
        array_name = os.path.splitext(os.path.basename(wav))[0]

        f = sf.SoundFile(wav)
        data = f.read()
        if args.stereo:
            data = data.flatten()
        else:
            data = convert_to_mono(data, f.channels)

        array_to_header(data, h_filename, array_name, args.format)
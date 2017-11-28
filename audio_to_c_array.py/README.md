audio_to_c_array.py
===================

Just a quick and dirty script, which, as its name suggests, takes an audio file (intended for PCM 24b encoded files), and outputs a C header file containing the audio samples in a C array.

Stereo: It can convert to mono, or output interleave.
Depth: Choose between int, or float, or altu8.

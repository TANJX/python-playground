from os import listdir
from os.path import isfile, join
from pydub import AudioSegment

input_path = '/Users/marstanjx/Desktop/audio/'
output_path = '/Users/marstanjx/Desktop/audio_out/'
all_audio = [f for f in listdir(input_path) if isfile(join(input_path, f))]
length = len(all_audio)

count = 0
for file in all_audio:
    print("[" + str(round(count / length * 100, 2)) + "%] " + file)
    song = AudioSegment.from_mp3(input_path + file)
    song += 4.5
    song.export(output_path + file, format="mp3")
    count += 1

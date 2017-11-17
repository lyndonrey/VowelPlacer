#import AudioSegment from pydub
import sys, glob

# The input directory must be in quotes (in Bash anyway) or else it wildcards weird
directory = '*.wav' 
# Get all the wav files from directory to parse
wavs = glob(directory)

cutLength = sys.argv[2]
for wav in wavs:
    time = 0
    index = 0
    while True: 
        try:
            endTime = time + cutLength #Works in milliseconds
                newAudio = AudioSegment.from_wav(wav)
                newAudio = newAudio[time:endTime]
                newAudio.export(wav + "cut" + index + ".wav", format="wav")
                time = endTime
        except:
            break
from os import path
from pydub import AudioSegment

src = "../boxedin_levelcomplete.mp3"
dst = "../boxedin_levelcomplete.wav"
# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
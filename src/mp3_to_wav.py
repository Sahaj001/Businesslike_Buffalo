from os import path
from pydub import AudioSegment

src = "/Users/sahajsingh/Downloads/Businesslike_Buffalo-layout-with-rendering/intro_music.mp3"
dst = "/Users/sahajsingh/Downloads/Businesslike_Buffalo-layout-with-rendering/intro_music.wav"
# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
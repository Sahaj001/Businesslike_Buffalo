"""
This is class for playing diff. sounds in our game
"""
from gtts import gTTS
import simpleaudio as sa
import playsound
path = "intro_music.wav"


class PlayAudio:
    """
    This class play audio using the path
    """
    def __init__(self, path: str) -> None:

        self.path = "intro_music.wav"

        self.wave_obj = sa.WaveObject.from_wave_file(self.path)

    def play(self):
        play_obj = self.wave_obj.play()
        play_obj.wait_done()


class TTAudio:
    """
    Converts the given text to audio
    """
    def __init__(self, text: str) -> None:
        self.text = text
        self.language = 'en'
        self.myobj = gTTS(text=self.text, lang=self.language, slow=False)
        self.myobj.save('text_audio.mp3')

    def play(self):
        self.audio = sa.WaveObject.from_wave_file('intro_music.wav')
        self.audio.play()


if __name__ == "__main__":

    # fc.LeftRightCheck.run()
    playsound.playsound('intro_music.mp3')

    # text = "hello welcome to boxed in"
    # text_audio = TTAudio(text)
    # text_audio.play()
    # audio1 = PlayAudio(path)
    # audio1.play()

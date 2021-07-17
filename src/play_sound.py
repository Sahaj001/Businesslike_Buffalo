"""This is class for playing diff. sounds in our game."""
import simpleaudio as sa
from gtts import gTTS


class PlayAudio:
    """This class play audio using the path."""

    def __init__(self, path_: str) -> None:

        self.path = path_

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
        self.myobj.save('assets/audio/text_audio.mp3')

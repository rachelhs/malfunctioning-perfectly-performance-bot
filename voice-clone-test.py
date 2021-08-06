from spokestack.tts.manager import TextToSpeechManager
from spokestack.tts.clients.spokestack import TextToSpeechClient
from spokestack.io.pyaudio import PyAudioOutput

from decouple import config
SPOKESTACK_ID = config("SPOKESTACK_ID")
SPOKESTACK_KEY = config("SPOKESTACK_KEY")

client = TextToSpeechClient(SPOKESTACK_ID, SPOKESTACK_KEY)
output = PyAudioOutput()
manager = TextToSpeechManager(client, output)
manager.synthesize("my name is rachel smith good morning how are you tonight?", voice="rachel-s")